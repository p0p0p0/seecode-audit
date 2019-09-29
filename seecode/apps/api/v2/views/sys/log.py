# coding: utf-8
import ast

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from seecode.libs.utils.api_response import JsonResponse
from seecode.libs.dal.syslog import create_syslog_obj
from seecode.libs.core.enum import LOG_LEVEL
from seecode.libs.core.settings import RSA
from seecode.libs.dal.config import get_config
from seecode.libs.core.exceptions import SeeCodeMissingImportantParameters


class SysLogSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """

        :param request:
        :return:
        """
        try:
            if 'application/json' not in request.content_type:
                raise Exception(u'"Content-type" 格式必须为 json 格式, 当前格式: {0}'.format(request.content_type))

            secret = request.data.get("secret", None)
            title = request.data.get("title", None)
            description = request.data.get("description", None)
            stack_trace = request.data.get("stack_trace", None)
            module_id = request.data.get("module_id", None)
            object_id = request.data.get("object_id", None)
            ipv4 = request.data.get("ipv4", None)
            sys_type = request.data.get("sys_type", 1)
            level = request.data.get("level", LOG_LEVEL.INFO)

            if secret:
                decrypt_str = RSA.decrypt_str(secret)
                json_data = ast.literal_eval(decrypt_str.decode('utf-8'))
                if 'title' in json_data:
                    title = json_data['title']
                if 'description' in json_data:
                    description = json_data['description']
                if 'stack_trace' in json_data:
                    stack_trace = json_data['stack_trace']
                if 'sys_type' in json_data:
                    sys_type = json_data['sys_type']
                if 'level' in json_data:
                    level = json_data['level']
                module_id = request.data.get("module_id", None)
                object_id = request.data.get("object_id", None)

            if not all((title, description)):
                raise SeeCodeMissingImportantParameters("Parameter 'title, description' content is invalid.")

            if not ipv4:
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ipv4 = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ipv4 = request.META['REMOTE_ADDR']

            create_syslog_obj(
                title=title,
                description=description,
                stack_trace=stack_trace,
                module_id=module_id,
                object_id=object_id,
                ipv4=ipv4,
                sys_type=sys_type,
                level=level,
            )
            return JsonResponse(
                data={
                },
                desc='更新成功',
                status=status.HTTP_200_OK,
                code=1
            )
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )
