# coding: utf-8

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from seecode.libs.utils.api_response import JsonResponse
from seecode.libs.dal.scan_task import get_task_by_id
from seecode.libs.dal.issue import create_or_update
from seecode.libs.dal.tactic import get_tactic_by_key
from seecode.libs.dal.issue import update_issue_obj
from seecode.libs.core.exceptions import SeeCodeMissingImportantParameters
from seecode.libs.dal.syslog import create_syslog_obj
from seecode.libs.core.enum import LOG_LEVEL


class IssueSet(APIView):
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
            issues = request.data.get("issues", None)

            if not all((task, issues)):
                raise SeeCodeMissingImportantParameters("Parameter 'task_id, issues' content is invalid.")

            for i in issues:
                tactic_obj = get_tactic_by_key(key=i['rule_key'])
                if tactic_obj and tactic_obj.is_active:
                    issue_obj = create_or_update(
                        app_obj=task.app,
                        rule_key=i['rule_key'],
                        file_name=i['file'],
                        start_line=i['start_line'],
                        end_line=i['end_line'],
                        scanner_id=i['engine'],
                        title=i['title'],
                        report_detail_url=i['report'],
                        last_commit=i['hash'],
                        last_commit_author=i['author'],
                        last_commit_author_email=i['author_email'],
                        code_segment=i['code_example'],
                        evidence_content=i['evidence_content'],
                        is_false_positive=i['is_false_positive'],
                        whitelist_rule_id=i['whitelist_rule_id'],
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
            import traceback;
            traceback.print_exc()
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )


class IssueCallbackSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, issue_id):
        """

        :param request:
        :param issue_id:
        :return:
        """
        try:
            if 'application/json' not in request.content_type:
                raise Exception(u'"Content-type" 格式必须为 json 格式, 当前格式: {0}'.format(request.content_type))

            scm_id = request.data.get("scm_id", None)
            scm_status = request.data.get("scm_status", None)
            scm_url = request.data.get("scm_url", None)

            update_issue_obj(
                issue_id=issue_id,
                scm_id=scm_id,
                scm_status=scm_status,
                scm_url=scm_url,
            )

            return JsonResponse(
                data={
                    'issue_id': issue_id
                },
                desc='更新成功',
                status=status.HTTP_200_OK,
                code=1
            )
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            create_syslog_obj(
                title='[IssueCallbackSet] 调用接口发生错误',
                description=str(ex),
                stack_trace=traceback.format_exc(),
                sys_type=1,
                level=LOG_LEVEL.CRITICAL
            )
            return JsonResponse(
                desc=str(ex),
                code=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_200_OK
            )
