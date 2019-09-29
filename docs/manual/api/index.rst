
============
API 接口
============

1. 认证
==============

确保 HTTP 请求中携带 Authorization 头，内容格式为："``Token *********``"，其中 Token 可以通过登录系统中的个人账号中获得。


.. code-block::  console

    "Authorization": "Token *********"

----

2. 升级
==============

2.1 查询升级信息
---------------------

.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/upgrade/version/``

.. response :

* **响应**


返回非加密内容：

.. code-block:: json

    {
        "code": 200,
        "data": {
            "version": "1.85.22",
            "md5": "1c0854e4c49646ebcd20ea586b8fc3f8",
            "release_time": "2019-09-20T02:54:31.205098+00:00",
            "download_path": "/home/seecode/upgrade/1.85.22.tgz",
            "download_type": "ftp"
        }
    }

返回加密内容：

.. code-block:: json

  {
    "code": 200,
    "data": {
        "secret": "WSoZvXo7RwEGJP1YsZ+2ylcD/WusnXMIKNb96GsDjTEzsivjrWRVsQN9tcDY5j6K4d2Qz1q0k5oaMfxSvyii0Hw8A9EF5Xtz5PokJ90OZtVUQAr6OK6CPumnaq77Dflx5OPuNPCNjf2267yyHY9AXCQV6Q5x/B0JOqZl/Se7/uTQvTgXPPyroXILo8gl2ZwI1GM1LlebDC0gELZgvv0+rbOWbNSeLbX0FcLaQYDuPUNBUXte1H4QZglhr5vkvNwCQv1MhW9XdRSjkYzwZYM0mBVzR1Db2XS6RWJYJAlOOKevdcrmF+iJCrF96kJPrlqalLACyhbAt/6MlPZ35tC+Mg=="
    }
  }


------

2. 任务
==============

2.1 查询扫描任务
---------------------


.. request :

* **请求**

  - 方式：``GET``
  - URI：``/api/v2/task/:task_id/``
  - 参数：

    - task_id： [整型] 扫描任务的ID

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. response :

* **响应**


返回内容：

.. code-block:: json

    {
        "code": 200,
        "data": {
            "task_id": 1862,
            "project_name": "tightMdmV2",
            "group_name": "默认扫描分组",
            "status": 1,
            "executor_ip": "192.168.1.1"
        },
        "desc": "成功！"
    }

----

2.2 创建扫描任务
---------------------



.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/scan/add/``
  - 参数：

    - ssh_url： [字符串] ssh 地址
    - branch： [字符串] 分支
    - app_name： [字符串] 应用名称
    - force_scan： [整型] 是否强制扫描，1 强制，0 不强制

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. code-block:: json

    {
        "ssh_url":"git@github.com:seecode-audit/vuln_java.git",
        "branch": "master",
        "app_name":"vuln_java",
        "force_scan": 0
    }

* **响应**


返回内容：

.. code-block:: json

    {
        "code": 200,
        "desc": "成功！"
    }

----

2.3 更新扫描状态
---------------------



.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/task/:task_id/status/``
  - 参数：

    - task_id： [整型] 扫描任务的ID
    - status： [整型] 状态码
    - end_time： [字符串] 结束时间
    - title： [字符串] 状态阶段
    - reason： [字符串] 原因

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到


.. code-block:: json

    {
        "status": 1,
        "end_time":"2019-07-30 09:37:03",
        "title":"扫描失败",
        "reason":"没有找到sonar-scanner。"
    }


* **响应**


返回内容：

.. code-block:: json

    {
        "code": 200,
        "desc": "成功！"
    }

----

2.4 更新统计信息
---------------------

.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/task/:task_id/statistic/``
  - 参数：

    - task_id： [整型] 扫描任务的ID
    - size： [整型] 项目大小 KB
    - total： [整型] 代码总行数
    - language： [字符串] 项目开发语言
    - statistics： 文件统计信息

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. code-block:: json

    {
        "size": 80,
        "total": 2048,
        "language":"java",
        "statistics":[
            {
                "language": "java",
                "files": 2,
                "blank": 300,
                "comment": 200,
                "code": 100
            },
            {
                "language": "python",
                "files": 2,
                "blank": 100,
                "comment": 20,
                "code": 103
            }
        ]
    }

.. response :

* **响应**


返回内容：

.. code-block:: json

    {
        "code": 200,
        "desc": "成功！"
    }

----


2.5 更新依赖组件
---------------------

.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/task/:task_id/component/``
  - 参数：

    - task_id： [整型] 扫描任务的ID

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. response :

* **响应**

.. code-block:: json

    [
      {
         "name": "fastjson",
         "tag": "com.alibaba",
         "version": "1.2.58",
         "new_version": "",
         "origin": "pom.xml"
      }
    ]



返回内容：

.. code-block:: json

    {
        "code": 200,
        "desc": "成功！"
    }

----

2.6 更新漏洞信息
---------------------



.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/task/:task_id/issues/``
  - 参数：

    - task_id： [整型] 扫描任务的ID
    - rule_key： [字符串] 规则 key
    - risk_id： [整型] 风险 id
    - category： [字符串] 漏洞类型
    - title： [字符串] 漏洞标标题
    - file： [字符串] 漏洞文件
    - author： [字符串] 最后提交作者
    - author_email： [字符串] 邮箱
    - hash： [字符串] 最后 commit id
    - start_line： [整型] 开始行
    - end_line： [整型] 结束行
    - report： [字符串] 报告
    - code_example： [字符串] 代码片段
    - is_false_positive： [布尔] 是否误报
    - whitelist_rule_id： [整型] 白名单 ID
    - evidence_content： [字符串] 取证内容
    - engine： [整型] 引擎 ID

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. response :

.. code-block:: json

    [
      {
        "rule_key": "java:jackson-databind-cve-2019-12384",
        "risk_id": 3,
        "category": "vulnerability",
        "title": "Jackson-databind \u53cd\u5e8f\u5217\u5316\u6f0f\u6d1e (CVE-2019-12384)",
        "file": "pom.xml",
        "author": "zhangsan",
        "author_email": "zhangsan@example.com",
        "hash": "182fb49613656f833ed4c5ed059e7855269e56f2",
        "start_line": 61,
        "end_line": 62,
        "report": "https://git.example.com/app_group/app/blob/master/pom.xml#L61",
        "code_example": "\n        <jackson.version>2.9.9</jackson.version>\n        <jackson-databind.version>2.9.9.3</jackson-databind.version>\n        <dealer.lib.version>2018.08.29.1730</dealer.lib.version>\n\n",
        "is_false_positive": false,
        "whitelist_rule_id": "",
        "evidence_content": "2.9.9",
        "engine": 2
      }
    ]


* **响应**


返回内容：

.. code-block:: json


    {
        "code": 200,
        "desc": "成功！"
    }

----

3. 系统
==============

3.1 日志收集
---------------------



.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/sys/log/``
  - 参数：

    - title： [字符串] 标题
    - description： [字符串] 描述
    - stack_trace： [字符串] 堆栈信息
    - sys_type： [字符串] 类型
    - level： [字符串] 级别

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. response :

.. code-block:: json

    {
        "title": "",
        "description": "",
        "stack_trace": "",
        "sys_type": "",
        "level": ""
    }

* **响应**


返回内容：

.. code-block:: json

    {
        "code": 200,
        "desc": "成功！"
    }

----

3.1 扫描节点注册
---------------------



.. request :

* **请求**

  - 方式：``POST``
  - URI：``/api/v2/node/host/``
  - 参数：

    - hostname： [字符串] 主机名称
    - ipv4： [字符串] ipv4 地址
    - ipv6： [字符串] ipv6 地址
    - role： [字符串] 角色
    - ui_version： [字符串] UI 版本
    - client_version： [字符串] 客户端版本

  - 状态码：

    - 200： 返回成功
    - 400： 参数错误
    - 401： 无效 token
    - 404： 项目未找到

.. response :

.. code-block:: json

    {
        "hostname": "test.local",
        "ipv4": "192.168.1.1",
        "ipv6": "",
        "role": "client",
        "ui_version": "",
        "client_version": "1.8.22"
    }

* **响应**


返回内容：

.. code-block:: json

    {
        "code": 200,
        "desc": "成功！"
    }
