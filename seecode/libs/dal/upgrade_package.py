# coding: utf-8
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.cache import cache

from seecode.apps.node.models import UpgradePackageInfo
from seecode.apps.scan.models import ScanProfileInfo
from seecode.libs.core.common import make_tar
from seecode.libs.core.common import make_dir
from seecode.libs.core.common import hash_md5_file
from seecode.libs.core.common import clean_dir
from seecode.libs.core.rsaencrypt import RSAEncrypt
from seecode.libs.dal.scan_profile import dump_scan_template
from seecode.libs.dal.upgrade_changelog import get_changelog
from seecode.libs.dal.upgrade_changelog import release_version
from seecode.libs.dal.upgrade_changelog import make_changelog_markdown
from seecode.libs.dal.upgrade_version import get_current_client_version
from seecode.libs.units import close_old_connections
from seecode.libs.core.cache_key import UPGRADE_CACHE
from seecode.libs.core.enum import LOG_LEVEL
from seecode.libs.utils.ftpwrapper import FTPWork
from seecode.libs.dal.syslog import create_syslog_obj
from seecode.libs.core.data import conf
from seecode.libs.core.enum import NODE_ROLE_TYPE
from seecode.libs.dal.config import get_config


def create_package_obj(**kwargs):
    """
    :param kwargs:
    :return:
    """
    description = kwargs.get('description', None)

    close_old_connections()
    version_obj = get_current_client_version()
    ver_no = '{0}.{1}.{2}'.format(version_obj.major, version_obj.minor, version_obj.revision)

    is_release_ver_no = UpgradePackageInfo.objects.filter(version=ver_no).first()
    if not is_release_ver_no:
        rsa = RSAEncrypt()
        scan_profile_list = ScanProfileInfo.objects.filter()
        if not scan_profile_list:
            raise Exception("未找到任何扫描模板.")

        # init path
        upgrade_path = os.path.join(settings.UPGRADE_ROOT, ver_no)
        dist_upgrade_path = os.path.join(settings.UPGRADE_ROOT, 'dist/', ver_no)
        make_dir([settings.UPGRADE_ROOT, upgrade_path, dist_upgrade_path])
        clean_dir(upgrade_path)

        # create xml file
        for profile in scan_profile_list:
            dump_scan_template(profile_id=profile.id, dump_path=upgrade_path)

        # original upgrade package
        file_name = 'sca_rule_v{0}_upgrade.tgz'.format(ver_no)
        make_tar(file_path=upgrade_path, save_path=settings.UPGRADE_ROOT, file_name=file_name)

        # RSA encryption upgrade package
        tar_full_path = os.path.join(settings.UPGRADE_ROOT, file_name)
        filename, _ = os.path.splitext(os.path.basename(tar_full_path))
        dist_package = os.path.join(dist_upgrade_path, '{0}.bin'.format(filename))
        rsa.encrypt_file(tar_full_path, save_path=dist_package)

        md5 = hash_md5_file(tar_full_path)
        if md5:
            with open(os.path.join(dist_upgrade_path, 'md5'), 'wb') as fp:
                fp.write(md5.encode("utf-8"))
        make_tar(file_path=dist_upgrade_path, save_path=dist_upgrade_path, file_name=file_name)
        file_path = os.path.join(dist_upgrade_path, file_name)
        save_path = __upload_upgrade(file_path, '{0}.tgz'.format(ver_no))
        # TODO sign
        upgrade = UpgradePackageInfo(
            name=file_name,
            version=ver_no,
            changelog=make_changelog_markdown(get_changelog(), ver_no),
            description=description,
            hash=md5,
            path=save_path or file_path,
            role=2
        )
        upgrade.save()
        release_version(ver_no)
        cache.set(UPGRADE_CACHE[3], None, 0)
        return upgrade


def get_last_client_package():
    """
    获取最新的client升级包
    :return:
    """
    cached = cache.get(UPGRADE_CACHE[3])
    if cached:
        return cached
    obj = UpgradePackageInfo.objects.filter(role=2, is_archive=False).order_by("-created_at").first()
    cache.set(UPGRADE_CACHE[3], obj, UPGRADE_CACHE[0])
    return obj


def __upload_upgrade(local_file, remote_file):
    """

    :param local_file:
    :param remote_file:
    :return:
    """
    try:
        web_conf = get_config()
        if web_conf['project']['upload_type'] == 2:
            ftp = FTPWork(
                host=web_conf['project']['ftp_host'],
                port=web_conf['project']['ftp_port'],
                username=web_conf['project']['ftp_username'],
                password=web_conf['project']['ftp_password'],
                debug=False
            )
            upgrade_path = os.path.join(web_conf['project']['ftp_path'], 'upgrade')
            ftp.make_dir(upgrade_path)
            remote_file = os.path.join(upgrade_path, remote_file)
            for i in range(0, 3):
                try:
                    ftp.upload_file(local_file, remote_file)
                    size = ftp.get_size(remote_file)
                    if size:
                        break
                except Exception as ex:
                    if i == 2:
                        raise ex
            ftp.close()
            create_syslog_obj(
                title='上传升级包成功',
                description=remote_file,
                level=LOG_LEVEL.INFO
            )
            return 'ftp://{0}:{1}{2}'.format(
                web_conf['project']['ftp_host'],
                web_conf['project']['ftp_port'],
                os.path.join(upgrade_path, remote_file)
            )
    except Exception as ex:
        import traceback
        create_syslog_obj(
            title='上传升级包失败',
            description=str(ex),
            stack_trace=traceback.format_exc(),
            level=LOG_LEVEL.ERROR
        )
        return None
