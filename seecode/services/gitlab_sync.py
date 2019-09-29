# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import traceback

from seecode.libs.core.data import logger
from seecode.celeryctl import celery_app
from seecode.libs.dal.syslog import create_syslog_obj
from seecode.libs.utils.gitlabwrapper import GitLabOperator
from seecode.libs.core.enum import LOG_LEVEL


@celery_app.task(ignore_result=True)
def start(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    try:
        logger.info('开始同步 GitLab 项目...')
        start_time = time.time()
        gitlab = GitLabOperator()
        gitlab.add_projects()
        end_time = time.time() - start_time
        create_syslog_obj(
            title='GitLab 项目同步成功',
            description='共计耗时:{0} 分钟'.format(round(end_time/60, 2)),
            level=LOG_LEVEL.NOTIFICATION
        )
        return True
    except Exception as ex:
        traceback.print_exc()
        create_syslog_obj(
            title='GitLab 同步失败',
            description=ex,
            stack_trace=traceback.format_exc(),
            level=1,
        )
        return False
