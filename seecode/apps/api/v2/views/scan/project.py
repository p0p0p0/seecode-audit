# coding: utf-8

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from seecode.libs.core.exceptions import SeeCodeMissingImportantParameters
from seecode.libs.units import parse_bool
from seecode.libs.dal.gitlab_project import get_project_by_ssh_url
from seecode.libs.dal.application import get_app_by_app_name
from seecode.libs.dal.application import get_app_by_branch
from seecode.libs.dal.application import create_app_obj
from seecode.libs.dal.scan_group import get_default_group
from seecode.libs.dal.gitlab_repository import get_repository_by_name
from seecode.libs.utils.api_response import JsonResponse
from seecode.libs.core.dispatchctl import create_scan_task
from seecode.libs.core.dispatchctl import send_task
from seecode.libs.core.enum import task_type as tasktype


class ProjectSet(APIView):
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

            ssh_url = request.data.get("ssh_url", None)
            branch = request.data.get("branch", "master")
            app_name = request.data.get("app_name", None)
            force_scan = request.data.get("force_scan", False)
            app_obj = None

            if not all((ssh_url, branch)):
                raise SeeCodeMissingImportantParameters("Missing 'ssh_url, branch' parameter.")

            project_obj = get_project_by_ssh_url(ssh_url=ssh_url)

            if not project_obj:
                raise Exception("'{0}' project not found.".format(ssh_url))

            if app_name:
                app_obj = get_app_by_app_name(name=app_name, project_id=project_obj.id)

            if not app_obj:
                repo_obj = get_repository_by_name(name=branch, project_id=project_obj.id)
                if app_name:
                    # FIXME 分支是否存在，不存在进行同步
                    if not repo_obj:
                        raise Exception("No '{0}' branch found.".format(branch))
                    app_name = app_name or branch
                    app_obj = create_app_obj(
                        project_obj=project_obj,
                        repo_obj=repo_obj,
                        module_name=app_name,
                        app_name=app_name
                    )
                else:
                    app_obj = get_app_by_branch(name=branch, project_id=project_obj.id)
                    if not app_obj:
                        app_obj = create_app_obj(
                            project_obj=project_obj,
                            repo_obj=repo_obj,
                            module_name=branch,
                            app_name=branch
                        )
            if not app_obj:
                code, message = -1, '创建扫描任务失败'
            else:
                task_group = get_default_group()
                task_obj = create_scan_task(
                    task_group_id=task_group.id,
                    app_id=app_obj.id,
                    is_force_scan=True,
                    scan_way=2,
                    version='v1',
                )
                send_task(task_id=task_obj.id)

                if task_obj:
                    code,  message = 1, '创建扫描任务成功'

            return JsonResponse(
                data={
                    'project_name': project_obj.name,
                    'branch': branch
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
