# coding: utf-8
"""
 gitlab api Handler
"""

import warnings

import requests

from seecode.libs.core.data import logger
# UserWarning
warnings.filterwarnings(action="ignore", message=".*Adding certificate verification is.*", category=Warning)


class GitlabAPIHandler(object):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def __init__(self, token=None, api_url=None):
        self.session = requests.Session()
        self.session.headers.update({'PRIVATE-TOKEN': token})
        self.gitlab_server = api_url

        if not self.gitlab_server.endswith('/'):
            self.gitlab_server = '{0}/'.format(self.gitlab_server)

    def _get_groups(self, page=1, per_page=100):
        """
        获得分页分组
        :param page: 当前页
        :param per_page: 页容量
        :return:
        """
        try:
            api_url = self.gitlab_server + 'groups?per_page={0}&page={1}'.format(per_page, page)
            resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

            if resp.status_code == 200:
                if 'X-Total-Pages' in resp.headers:
                    total_page = int(resp.headers['X-Total-Pages'])
                else:
                    total_page = 1
                return resp.status_code, total_page, resp.json()
            else:
                return resp.status_code, -1, resp.reason
        except Exception as ex:
            return -1, -1, ex

    def get_groups(self):
        """
        获得所有分组
        :return:
        """
        result = []

        page_size = 100
        status_code, total_page, contents = self._get_groups(per_page=page_size)

        for page in range(1, total_page + 1):
            if page != 1:
                status_code, _, contents = self._get_groups(per_page=page_size, page=page)
            if status_code == 200:
                result.extend(contents)
            else:
                logger.warning('同步项目分组发生错误, {0}'.format(contents))
        return result

    def _get_group_info(self, group_id):
        """

        :param group_id:
        :return:
        """
        try:
            api_url = self.gitlab_server + 'groups/{0}'.format(group_id)
            resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

            if resp.status_code == 200:
                return resp.status_code, resp.json()
            else:
                return resp.status_code, resp.reason
        except Exception as ex:
            return -1, ex

    def get_group_info(self, group_id):
        """

        :param group_id:
        :return:
        """
        result = None
        status_code, resp = self._get_group_info(group_id=group_id)

        if status_code == 200:
            result = resp

        return result

    def _get_projects_by_group(self, group_id, page=1, per_page=100):
        """
        获得指定分组下的所有项目
        :param group_id: 分组id
        :param page: 当前页
        :param per_page: 页容量
        :return:
        """
        api_url = self.gitlab_server + 'groups/{0}/projects?per_page={1}&page={2}'.format(group_id, per_page, page)
        resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

        if resp.status_code == 200:
            if 'X-Total-Pages' in resp.headers:
                total_page = int(resp.headers['X-Total-Pages'])
            else:
                total_page = 1
            return resp.status_code, total_page, resp.json()
        else:
            return resp.status_code, -1, resp.reason

    def get_projects_by_group(self, group_id):
        """
        获得指定分组下的所有项目
        :param group_id: 分组id
        :return:
        """
        result = []

        page_size = 100
        status_code, total_page, contents = self._get_projects_by_group(group_id=group_id, per_page=page_size)

        for page in range(1, total_page + 1):
            if page != 1:
                status_code, _, contents = self._get_projects_by_group(
                    group_id=group_id, per_page=page_size, page=page)
            if status_code == 200:
                result.extend(contents)
            else:
                logger.warning('同步项目发生错误, {0}'.format(contents))
        return result

    def _get_projects(self, page=1, per_page=100):
        """
        获得的所有项目
        :param page: 当前页
        :param per_page: 页容量
        :return:
        """
        try:

            api_url = self.gitlab_server + '/projects?per_page={0}&page={1}'.format(per_page, page)
            resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

            if resp.status_code == 200:
                if 'X-Total-Pages' in resp.headers:
                    total_page = int(resp.headers['X-Total-Pages'])
                else:
                    total_page = 1
                return resp.status_code, total_page, resp.json()
            else:
                return resp.status_code, -1, resp.reason
        except Exception as ex:
            return -1, -1, ex

    def get_projects(self):
        """
        :return:
        """
        try:
            page_size = 100
            status_code, total_page, contents = self._get_projects(per_page=page_size)

            for page in range(1, total_page + 1):
                try:
                    if page != 1:
                        status_code, _, contents = self._get_projects(per_page=page_size, page=page)
                    if status_code == 200:
                        for item in contents:
                            yield item
                    else:
                        logger.warning('同步项目发生错误, {0}'.format(contents))
                except:
                    pass
        except Exception as ex:
            logger.error(ex)


    def get_project_info(self, project_id):
        """
        获得指定项目信息
        :param project_id: 项目id
        :return:
        """
        api_url = self.gitlab_server + 'projects/{0}'.format(project_id)
        resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

        if resp.status_code == 200:
            return resp.status_code, resp.json()
        else:
            return resp.status_code, resp.reason

    def _get_branches(self, project_id, page=1, per_page=100):
        """
        获取项目中的 branches, https://git.example.com/api/v3/projects/:id/repository/branches
        :param project_id:
        :return:
        """
        try:
            api_url = self.gitlab_server + 'projects/{0}/repository/branches?per_page={1}&page={2}'.format(
                project_id, per_page, page
            )
            resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

            if resp.status_code == 200:
                if 'X-Total-Pages' in resp.headers:
                    total_page = int(resp.headers['X-Total-Pages'])
                else:
                    total_page = 1
                return resp.status_code, total_page, resp.json()
            else:
                return resp.status_code, -1, resp.reason
        except Exception as ex:
            return -1, -1, ex

    def get_branches(self, project_id):
        """
        获取项目中的 branches, https://git.example.com/api/v3/projects/:id/repository/branches
        :param project_id:
        :return:
        """
        result = []

        page_size = 100
        status_code, total_page, contents = self._get_branches(project_id=project_id, per_page=page_size)

        for page in range(1, total_page + 1):
            if page != 1:
                status_code, _, contents = self._get_branches(
                    project_id=project_id, per_page=page_size, page=page)
            if status_code == 200:
                for item in contents:
                    yield item
            else:
                logger.warning('获取项目分支发生错误, {0}'.format(contents))
        return result

    def _get_members_by_group(self, group_id, page=1, per_page=100):
        """
        获得指定分组下的所有成员
        :param group_id: 分组id
        :param page: 当前页
        :param per_page: 页容量
        :return:
        """
        try:
            api_url = self.gitlab_server + 'groups/{0}/members?per_page={1}&page={2}'.format(group_id, per_page, page)
            resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

            if resp.status_code == 200:
                if 'X-Total-Pages' in resp.headers:
                    total_page = int(resp.headers['X-Total-Pages'])
                else:
                    total_page = 1
                return resp.status_code, total_page, resp.json()
            else:
                return resp.status_code, -1, resp.reason
        except Exception as ex:
            return -1, -1, ex

    def get_members_by_group(self, group_id):
        """
        获得指定分组下的所有成员
        :param group_id: 分组id
        :return:
        """
        result = []

        page_size = 100
        status_code, total_page, contents = self._get_members_by_group(group_id=group_id, per_page=page_size)

        for page in range(1, total_page + 1):
            if page != 1:
                status_code, _, contents = self._get_members_by_group(
                    group_id=group_id, per_page=page_size, page=page)
            if status_code == 200:
                result.extend(contents)
            else:
                logger.warning('同步分组成员发生错误, {0}'.format(contents))
        return result

    def _get_members_by_project(self, project_id, page=1, per_page=100):
        """
        获得指定分组下的所有成员
        :param project_id: 分组id
        :param page: 当前页
        :param per_page: 页容量
        :return:
        """
        try:
            api_url = self.gitlab_server + 'projects/{0}/members?per_page={1}&page={2}'.format(project_id, per_page,
                                                                                               page)
            resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

            if resp.status_code == 200:
                if 'X-Total-Pages' in resp.headers:
                    total_page = int(resp.headers['X-Total-Pages'])
                else:
                    total_page = 1
                return resp.status_code, total_page, resp.json()
            else:
                return resp.status_code, -1, resp.reason
        except Exception as ex:
            return -1, -1, ex

    def get_members_by_project(self, project_id):
        """
        获得指定分组下的所有成员
        :param project_id: 分组id
        :return:
        """
        page_size = 100
        status_code, total_page, contents = self._get_members_by_project(project_id=project_id, per_page=page_size)

        for page in range(1, total_page + 1):
            if page != 1:
                status_code, _, contents = self._get_members_by_project(
                    project_id=project_id, per_page=page_size, page=page)
            if status_code == 200:
                for item in contents:
                    yield item

    def get_member_info(self, user_id):
        """
        :param user_id:
        :return:
        """
        api_url = self.gitlab_server + 'users/{0}/'.format(user_id)
        resp = self.session.get(api_url, headers=self.HEADERS, verify=False)

        if resp.status_code == 200:
            return resp.status_code, resp.json()
        else:
            return resp.status_code, resp.reason

    def exist_branch_for_gitlab(self, branch_name, project_id):
        """

        :param branch_name:
        :param project_id:
        :return:
        """
        status_code, total_page, json = self.get_branches(project_id)

        if status_code == 200:
            for item in json:
                if item['name'] == branch_name:
                    return True
        return False
