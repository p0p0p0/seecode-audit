# coding: utf-8

import requests
import random
import time
import base64

from seecode.libs.core.exceptions import HTTPStatusCodeError
from seecode.libs.core.exceptions import SonarQubeAuthenticationFailed
from seecode.libs.core.data import logger as _logger
from seecode.libs.core.common import parse_int
from seecode.libs.core.common import get_total_page


class SonarAPIHandler(object):
    """
    support SonarQube 7.1
    """

    def __init__(self, **kwargs):
        token = kwargs.get('token', None)
        self.logger = kwargs.get("logger", _logger)
        self.sonar_server = kwargs.get('sonar_server', None)
        self.http_timeout_retry = parse_int(kwargs.get('http_timeout_retry'), 3)
        self.http_failed_retry = parse_int(kwargs.get('http_failed_retry'), 3)
        self.http_timeout = parse_int(kwargs.get('http_timeout'), 10)

        self.session = requests.Session()
        user_password = '{0}:{1}'.format(token, '')
        headers = {
            "Authorization": 'Basic {0}'.format(base64.b64encode(user_password.encode('utf-8')).decode("utf-8")),

        }

        self.session.headers.update(headers)
        if not self.sonar_server.endswith('/'):
            self.sonar_server = '{0}/'.format(self.sonar_server)

        if not self.__validate_authentication():
            msg = "The authentication failed. Please check if the token({0}) is correct.".format(token)
            raise SonarQubeAuthenticationFailed(msg)

    def __validate_authentication(self):
        """
        Validate the authentication credentials passed on client initialization.
        This can be used to test the connection, since API always returns 200.
        :return: True if valid
        """
        api_url = '{0}api/authentication/validate'.format(self.sonar_server)
        res = self.session.get(api_url).json()
        return res.get('valid', False)

    def __send_data(self, url, data=None, method='POST'):
        """

        :param url:
        :param data:
        :param method:
        :return:
        """
        def get_delay_s():
            return round(random.random(), 2) * random.randrange(3, 9)

        result = None
        try_index = 1
        while True:
            try:
                if method == 'GET':
                    resp = self.session.get(url, params=data, timeout=self.http_timeout, verify=False)
                else:
                    resp = self.session.post(url, json=data, timeout=self.http_timeout, verify=False)
                self.logger.debug("URL:{0}\nHeaders:{1}\nBody:{2}".format(resp.request.url, resp.request.headers, data))
                if resp.status_code == 200:
                    result = resp.json()
                    break
                else:
                    self.logger.warning('status_code:{0}, reason:{1}'.format(resp.status_code, resp.reason))
                    raise HTTPStatusCodeError(resp.reason)

            except (requests.exceptions.Timeout, requests.exceptions.ProxyError, HTTPStatusCodeError) as ex:
                self.logger.error(ex)
                time.sleep(get_delay_s())

                if try_index >= self.http_failed_retry+1:
                    break
                else:
                    self.logger.warning('[-] Start {0} attempts to send data...'.format(try_index))
                    try_index += 1

        return result

    def get_components_search(self, qualifiers="TRK"):
        """
        获得所有 components
        :param qualifiers:
                   BRC - Sub-projects
                   DIR - Directories
                   FIL - Files
                   TRK - Projects
                   UTS - Unit Test Files
        :return:
        """
        api_url = '{0}api/components/search'.format(self.sonar_server)
        page_size = 200
        data = {
            # 'language': '',  # py, c, cpp, objc, css, scss, less, js, cs, java, grvy
            'p': 1,
            'ps': page_size,
            # 'q': '',
            'qualifiers': qualifiers
        }

        resp = self.__send_data(url=api_url, data=data, method='GET')
        if resp:
            total = resp['paging']['total']
            total_page = get_total_page(total, page_size)
            for page in range(1, total_page + 1):
                if page != 1:
                    data['p'] = page
                    resp = self.__send_data(url=api_url, data=data, method='GET')
                if resp:
                    yield resp['components']

    def get_components_show(self, component):
        """
        :param component:
        :return:
        """
        api_url = '{0}api/components/show'.format(self.sonar_server)
        data = {
            'component': component,
        }
        result = None
        resp = self.__send_data(url=api_url, data=data, method='GET')
        if resp:
            result = resp
        return result

    def get_ce_component(self, componentId, componentKey=None):
        """
        :param componentId:
        :param componentKey:
        :return:
        """
        api_url = '{0}api/ce/component'.format(self.sonar_server)
        data = {}
        if componentId:
            data['componentId'] = componentId
        if componentKey:
            data['componentKey'] = componentKey
        result = None
        resp = self.__send_data(url=api_url, data=data, method='GET')
        if resp:
            result = resp
        return result

    def get_issues(self, project_key, **kwargs):
        """
        获取项目的issue
        {
            "key": "01fc972e-2a3c-433e-bcae-0bd7f88f5123",
            "component": "com.github.kevinsawicki:http-request:com.github.kevinsawicki.http.HttpRequest",
            "project": "com.github.kevinsawicki:http-request",
            "rule": "checkstyle:com.puppycrawl.tools.checkstyle.checks.coding.MagicNumberCheck",
            "status": "RESOLVED",
            "resolution": "FALSE-POSITIVE",
            "severity": "MINOR",
            "message": "'3' is a magic number.",
            "line": 81,
            "hash": "a227e508d6646b55a086ee11d63b21e9",
            "author": "Developer 1",
            "effort": "2h1min",
            "creationDate": "2013-05-13T17:55:39+0200",
            "updateDate": "2013-05-13T17:55:39+0200",
            "tags": [
                "bug"
            ],
            "type": "RELIABILITY",
            "comments": [
                {
                    "key": "7d7c56f5-7b5a-41b9-87f8-36fa70caa5ba",
                    "login": "john.smith",
                    "htmlText": "Must be &quot;final&quot;!",
                    "markdown": "Must be \"final\"!",
                    "updatable": false,
                    "createdAt": "2013-05-13T18:08:34+0200"
                }
            ],
            "attr": {
                "jira-issue-key": "SONAR-1234"
            },
            "transitions": [
                "unconfirm",
                "resolve",
                "falsepositive"
            ],
            "actions": [
                "comment"
            ],
            "textRange": {
                "startLine": 2,
                "endLine": 2,
                "startOffset": 0,
                "endOffset": 204
            },
            "flows": [
                {
                    "locations": [
                        {
                            "textRange": {
                                "startLine": 16,
                                "endLine": 16,
                                "startOffset": 0,
                                "endOffset": 30
                            },
                            "msg": "Expected position: 5"
                        }
                    ]
                },
                {
                    "locations": [
                        {
                            "textRange": {
                                "startLine": 15,
                                "endLine": 15,
                                "startOffset": 0,
                                "endOffset": 37
                            },
                            "msg": "Expected position: 6"
                        }
                    ]
                }
            ]
        }
        :param project_key:
        :return:
        """
        ps = kwargs.get('ps', 200)
        severities = kwargs.get('severities', None)  # INFO MINOR MAJOR CRITICAL BLOCKER
        created_after = kwargs.get('created_after', None)
        types = kwargs.get('types', None)  # CODE_SMELL BUG VULNERABILITY

        api_url = '{0}api/issues/search'.format(self.sonar_server)
        data = {
            'projectKeys': project_key,
            'p': 1,
            'ps': int(ps),
            'statuses': 'OPEN',
        }
        if severities:
            data['severities'] = severities
        if types:
            data['types'] = types
        if created_after:
            data['createdAfter'] = created_after

        resp = self.__send_data(url=api_url, data=data, method='GET')

        if resp:
            total = resp['paging']['total']
            total_page = get_total_page(total, ps)
            for page in range(1, total_page + 1):
                if page != 1:
                    data['p'] = page
                    resp = self.__send_data(url=api_url, data=data, method='GET')
                if resp:
                    yield resp['issues']

    def get_rule_info(self, rule_key):
        """
        获取项目的rule
        :param rule_key:
        :return:
        """

        api_url = '{0}api/rules/show'.format(self.sonar_server)

        data = {
            'key': rule_key
        }
        resp = self.__send_data(url=api_url, data=data, method='GET')
        if resp:
            result = resp
        return result

    def get_plugins(self):
        """
        获取所有 plugins
        :return:
        """

        api_url = '{0}api/plugins/installed'.format(self.sonar_server)

        resp = self.__send_data(url=api_url, method='GET')
        if resp:
            yield resp['plugins']

    def get_rules(self, **kwargs):
        """
        获取所有的rules
        :return:

         {u'p': 1,
         u'ps': 100,
         u'rules': [{"key": "squid:S1067",
                      "repo": "squid",
                      "name": "Expressions should not be too complex",
                      "createdAt": "2013-03-27T08:52:40+0100",
                      "htmlDesc": "<p>\nThe complexity of an expression is defined by the number of <code>&&</code>, <code>||</code> and <code>condition ? ifTrue : ifFalse</code> operators it contains.\nA single expression's complexity should not become too high to keep the code readable.\n</p>\n\n<p>The following code, with a maximum complexity of 3:</p>\n\n<pre>\nif (condition1 && condition2 && condition3 && condition4) { /* ... */ }  // Non-Compliant\n</pre>\n\n<p>could be refactored into something like:</p>\n\n<pre>\nif (relevantMethodName1() && relevantMethodName2()) { /* ... */ }        // Compliant\n\n/* ... */\n\nprivate boolean relevantMethodName1() {\n  return condition1 && condition2;\n}\n\nprivate boolean relevantMethodName2() {\n  return condition3 && condition4;\n}\n</pre>",
                      "severity": "MAJOR",
                      "status": "READY",
                      "internalKey": "S1067",
                      "isTemplate": false,
                      "tags": [],
                      "sysTags": ["brain-overload"],
                      "lang": "java",
                      "langName": "Java",
                      "scope": "MAIN",
                      "type": "CODE_SMELL",
                      "params": [
                        {
                          "key": "max",
                          "desc": "Maximum number of allowed conditional operators in an expression",
                          "defaultValue": "3"
                        }
                      ]
                    }}],
         u'total': 5220}
        """
        page_size = 200
        data = {
            'p': 1,
            'ps': page_size,
        }
        qprofile = kwargs.get('qprofile', None)
        if qprofile:
            data['qprofile'] = qprofile

        api_url = '{0}api/rules/search'.format(self.sonar_server)

        resp = self.__send_data(url=api_url, data=data, method='GET')
        if resp:
            total = resp['total']
            total_page = get_total_page(total, page_size)
            for page in range(1, total_page + 1):
                if page != 1:
                    data['p'] = page
                    resp = self.__send_data(url=api_url, data=data, method='GET')
                if resp:
                    yield resp['rules']

    def get_languages(self):
        """
        获取所有的languages
        :return:
        """

        api_url = '{0}api/languages/list'.format(self.sonar_server)

        resp = self.__send_data(url=api_url, method='GET')
        if resp:
            yield resp['languages']

    def get_qualityprofiles(self):
        """
        获取所有的languages
        :return:
        """

        api_url = '{0}api/qualityprofiles/search'.format(self.sonar_server)
        resp = self.__send_data(url=api_url, method='GET')
        if resp:
            yield resp['profiles']
