# coding: utf-8
import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from seecode.libs.dal.scan_task import get_task_by_id
from seecode.libs.dal.scan_task import update_task_failed
from seecode.libs.dal.scan_task import update_task_scan_init
from seecode.libs.dal.scan_task import update_task_scan_component
from seecode.libs.dal.scan_task import update_task_start
from seecode.libs.dal.scan_task import update_task_success
from seecode.libs.dal.scan_task import update_task_title
from seecode.libs.dal.scan_task import update_task_statistics
from seecode.libs.utils.api_response import JsonResponse
from seecode.libs.core.common import parse_int
from seecode.libs.core.common import utc2local
from seecode.libs.core.exceptions import SeeCodeMissingImportantParameters


class TaskSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, task_id):
        """

        :param request:
        :param task_id:
        :return:
        """
        try:
            data = None
            task = get_task_by_id(task_id)
            status_code, message = status.HTTP_404_NOT_FOUND, "失败"

            if task:
                status_code = status.HTTP_200_OK
                message = "成功！"
                data = {
                    'task_id': task.id,
                    'project_name': task.app.project.name,
                    'group_name': task.group.name,
                    'status': task.status,
                    'executor_ip': task.executor_ip,
                }

            return JsonResponse(
                data=data,
                desc=message,
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
            task_status = request.data.get("status", None)
            end_time = request.data.get("end_time", None)
            start_time = request.data.get("start_time", None)
            executor_ip = request.data.get("executor_ip")

            if not all((task, task_status)):
                raise SeeCodeMissingImportantParameters("Missing 'task_id, status' parameter.")

            if end_time:
                end_time = utc2local(end_time)
            else:
                end_time = datetime.datetime.now()
            if start_time:
                start_time = utc2local(start_time)
            else:
                end_time = datetime.datetime.now()

            task_status = parse_int(task_status)
            code, message = -1, '更新失败'

            if task_status == 1:  # failed
                msg = request.data.get("msg", '')
                is_ok = update_task_failed(
                    task_id=task.id,
                    title='扫描任务失败',
                    reason=msg,
                    end_time=end_time
                )
                if is_ok:
                    code, message = 1, '更新成功'

            elif task_status == 3:  # init
                log_path = request.data.get("log_path", '')
                scan_template = request.data.get("scan_template", '')
                scan_template_version = request.data.get("scan_template_version", '')
                is_ok = update_task_scan_init(
                    task_id=task.id,
                    executor_ip=executor_ip,
                    scan_template=scan_template,
                    scan_template_version=scan_template_version,
                    start_time=start_time,
                    title='开始初始化扫描任务',
                    reason='',
                    log_path=log_path,
                )
                if is_ok:
                    code, message = 1, '更新成功'

            elif task_status == 4:  # component
                commit_hash = request.data.get("commit_hash")
                title = request.data.get("title", '开始同步项目代码')
                is_ok = update_task_scan_component(
                    task_id=task.id,
                    executor_ip=executor_ip,
                    commit_hash=commit_hash,
                    title=title,
                    reason='',
                )
                if is_ok:
                    code, message = 1, '更新成功'

            elif task_status == 5:  # start
                is_ok = update_task_start(
                    task_id=task.id,
                    executor_ip=executor_ip,
                    title='开始扫描代码',
                    reason='',
                )
                if is_ok:
                    code, message = 1, '更新成功'

            elif task_status == 6:  # success
                statistics = request.data.get("statistics", None)
                msg = request.data.get("msg")
                is_ok = update_task_success(
                    task_id=task.id,
                    executor_ip=executor_ip,
                    end_time=end_time,
                    title=msg,
                )
                try:
                    if statistics:
                        critical = statistics['critical'] or 0
                        high = statistics['high'] or 0
                        medium = statistics['medium'] or 0
                        low = statistics['low'] or 0
                        info = statistics['info'] or 0
                        scope = statistics['scope'] or 0
                        update_task_statistics(
                            task_id=task_id,
                            critical=critical,
                            high=high,
                            medium=medium,
                            low=low,
                            info=info,
                            scope=scope,
                        )
                except Exception as ex:
                    pass
                if is_ok:
                    code, message = 1, '更新成功'

            elif task_status == 7:  # message
                title = request.data.get("title", '')
                reason = request.data.get("reason", '')
                level = request.data.get("level", '')
                is_ok = update_task_title(
                    task_id=task.id,
                    title=title,
                    reason=reason,
                    level=level,
                )
                if is_ok:
                    code, message = 1, '更新成功'

            else:
                raise Exception("Parameter 'status' is out of range.")

            return JsonResponse(
                data={
                    'task_id': task.id
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
