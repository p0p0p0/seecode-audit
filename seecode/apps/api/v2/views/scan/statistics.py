# coding: utf-8

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from seecode.libs.dal.application import update_app_lang
from seecode.libs.dal.file_statistics import create_or_update
from seecode.libs.dal.scan_task import get_task_by_id
from seecode.libs.dal.dependent import create_or_update as d_create_or_update
from seecode.libs.utils.api_response import JsonResponse
from seecode.libs.core.exceptions import SeeCodeMissingImportantParameters


class FileStatisticSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, task_id):
        """

        :param request:
        :param task_id:
        :return:
        """
        try:
            if 'application/json' not in request.content_type:
                raise Exception(u'"Content-type" 格式必须为 json 格式, 当前格式: {0}'.format(request.content_type))

            task = get_task_by_id(task_id)

            if not all((task,)):
                raise SeeCodeMissingImportantParameters("Parameter 'task_id' content is invalid.")

            size = request.data.get("size")
            total = request.data.get("total")
            language = request.data.get("language")
            statistics = request.data.get("statistics")
            code, message = -1, '更新失败'

            is_ok = update_app_lang(
                app_id=task.app.id,
                code_total=total,
                size=size,
                lang=language,
                status=2
            )

            if is_ok:
                for s in statistics:
                    create_or_update(
                        app_obj=task.app,
                        language=s['language'],
                        files=s['files'],
                        blank=s['blank'],
                        comment=s['comment'],
                        code=s['code'],
                    )
                code, message = 1, '更新成功'

            return JsonResponse(
                data={
                    'task_id': task.id,
                    'app_id': task.app.id
                },
                desc=message,
                status=status.HTTP_200_OK,
                code=code
            )
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )


class ComponentSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, task_id):
        """

        :param request:
        :param task_id:
        :return:
        """
        try:
            if 'application/json' not in request.content_type:
                raise Exception(u'"Content-type" 格式必须为 json 格式, 当前格式: {0}'.format(request.content_type))

            task = get_task_by_id(task_id)
            components = request.data.get("components", None)

            if not all((task, components)):
                raise SeeCodeMissingImportantParameters("Parameter 'task_id, components' content is invalid.")
            # FIXME 添加归档功能
            for s in components:
                d_create_or_update(
                    app_obj=task.app,
                    name=s['name'],
                    group_id=s['tag'],
                    artifact_id=s['name'],
                    version=s['version'],
                    new_version=s['new_version'],
                    file_name=s['origin'],
                )

            return JsonResponse(
                data={
                    'task_id': task.id,
                    'app_id': task.app.id
                },
                desc='更新成功',
                status=status.HTTP_200_OK,
                code=1
            )
        except Exception as ex:
            import traceback;traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )
