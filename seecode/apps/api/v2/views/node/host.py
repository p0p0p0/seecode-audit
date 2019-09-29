# coding: utf-8

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from seecode.libs.dal.host import create_or_update_host
from seecode.libs.utils.api_response import JsonResponse


class HostSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        :return:

        """
        try:
            if 'application/json' not in request.content_type:
                raise Exception(u'"Content-type" 格式必须为 json 格式, 当前格式: {0}'.format(request.content_type))

            hostname = request.data.get('hostname', None)
            ipv4 = request.data.get('ipv4', None)
            ipv6 = request.data.get('ipv6', None)
            role = request.data.get('role', 'client')
            ui_version = request.data.get('ui_version', None)
            client_version = request.data.get('client_version', None)

            result = create_or_update_host(
                hostname=hostname,
                ipv4=ipv4,
                ipv6=ipv6,
                role=role,
                ui_version=ui_version,
                client_version=client_version,
            )

            if result:
                code = 1
                message = "成功！"
            else:
                code = -1
                message = "失败"
            return JsonResponse(data={
                'status': code,
                'message': message,
            }, code=status.HTTP_200_OK)
        except Exception as ex:
            import traceback; traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )
