# coding: utf-8

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from seecode.libs.dal.service import create_or_update_hostservice
from seecode.libs.utils.api_response import JsonResponse


class ServiceSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        :return:

        """
        try:
            if 'application/json' not in request.content_type:
                raise Exception(u'"Content-type" 格式必须为 json 格式, 当前格式: {0}'.format(request.content_type))

            ipv4 = request.data.get('ipv4', None)
            items = request.data.get('items', None)

            for item in items:
                result = create_or_update_hostservice(
                    ipv4=ipv4,
                    key=item['key'],
                    status=item['status'],
                    ppid=item['ppid'] if 'ppid' in item else None,
                    pid=item['pid'] if 'pid' in item else None,
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
            import traceback;
            traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )
