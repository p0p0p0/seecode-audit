# coding: utf-8

from urllib.parse import urlparse

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from seecode.libs.core.settings import RSA
from seecode.libs.dal.config import get_config
from seecode.libs.dal.upgrade_package import get_last_client_package
from seecode.libs.utils.api_response import JsonResponse


class UpgradeSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """

        :param request:
        :return:
        """
        try:
            web_config = get_config()
            data = None
            upgrade = get_last_client_package()

            if upgrade:
                download_path, download_type = upgrade.path, ''

                if upgrade.path:
                    if 'ftp' in upgrade.path:
                        download_path = urlparse(upgrade.path).path
                        download_type = 'ftp'

                status_code = status.HTTP_200_OK
                data = {
                    'version': upgrade.version,
                    'md5': upgrade.hash,
                    'release_time': upgrade.created_at.isoformat(),
                    'download_path': download_path,
                    'download_type': download_type,
                }
                if web_config['option']['seecode_node_secret']:
                    data = {
                        'secret': RSA.encrypt_str(str(data))
                    }
            else:
                status_code = status.HTTP_404_NOT_FOUND

            return JsonResponse(
                data=data,
                status=status_code,
                code=status_code
            )
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )
