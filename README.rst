
SeeCode Audit Community Edition
==========================================


.. image:: https://readthedocs.org/projects/seecode-audit/badge/?version=latest
    :target: https://seecode-audit.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/python-3.6|3.7-brightgreen.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/github/issues/seecode-audit/seecode-scanner.svg
    :alt: GitHub issues
    :target: https://github.com/seecode-audit/seecode-scanner/issues

.. image:: https://img.shields.io/github/forks/seecode-audit/seecode-scanner.svg
    :alt: GitHub forks
    :target: https://github.com/seecode-audit/seecode-scannernetwork

.. image:: https://img.shields.io/github/stars/seecode-audit/seecode-scanner.svg
    :alt: GitHub stars
    :target: https://github.com/Mseecode-audit/seecode-scanner/stargazers

.. image:: https://img.shields.io/github/license/seecode-audit/seecode-scanner.svg
    :alt: GitHub license
    :target: https://github.com/seecode-audit/seecode-scanner/blob/master/LICENSE


.. rtd-inclusion-marker-do-not-remove

``SeeCode Audit`` 是一套代码审计管理系统，该系统需要结合 `seecode-scanner <https://github.com/seecode-audit/seecode-scanner>`_
工具一起使用。 ``SeeCode Audit`` 是使用 Python3 + Django2 + MySQL + Redis/Memcached + Redis/RabbitMQ 技术搭建。

``SeeCode Audit`` 其最早的思路来源于 `《代码自动化审计系统的建设(上)》 <http://mykings.me/2018/08/07/code-automation-audit/>`_ 与
`《代码自动化审计系统的建设(下)》 <http://mykings.me/2018/09/05/code-automation-audit2/>`_ 文章，经过不断的打磨优化最后开发出 ``SeeCode Audit``
系统，并进行开源。


----

1. 功能特点
-------------

1.1 认证与授权
^^^^^^^^^^^^^^^^^

* 支持 SSO、Django authentication 等认证方式
* 支持基于 Django 框架的 RBAC 访问控制
* 支持基于 JWT Token 的 API 接口认证方式

1.2 项目与应用管理
^^^^^^^^^^^^^^^^^^^^^

* 支持线上（GitLab）项目信息同步与管理
* 支持项目时间轴历史记录与查看
* 支持项目应用创建，可为同一个项目不同分支创建不同应用
* 支持对应用的大小、开发语言、代码行数、依赖组件、组件版本的分析
* 支持依赖组件按照条件导出功能
* 支持对应用健康风险：危险、警告、安全的半定量评估
* 支持离线 ZIP 包项目扫描
* 支持扫描任务的 API 触发与手动触发方式

1.3 自定义扫描模板
^^^^^^^^^^^^^^^^^^^^^

* 支持扫描模板的高度自定义，同一个引擎可包含不同的扫描策略（规则、插件）
* 支持扫描引擎参数自定义
* 支持扫描引擎执行超时设定
* 支持扫描模板的版本控制

1.4 灵活的扫描规则与插件
^^^^^^^^^^^^^^^^^^^^^^^^^^

* 支持基于目录、文件、内容、组件等方式的自定义规则
* 支持基于正则表达式的内容检测方式
* 支持代码风格、坏味道、漏洞等不同类型设定
* 支持 Python 插件形式的检测方式
* 支持对扫描策略（规则、插件）的风险评分
* 支持扫描策略（规则、插件）的版本控制
* 支持项目依赖组件对已知漏洞识别能力

1.5 漏洞风险管理
^^^^^^^^^^^^^^^^^^^
* 支持对漏洞的生命周期管理
* 支持漏洞处理流程记录（历史操作记录）
* 支持漏洞文件提交作者、邮箱地址的分析
* 支持漏洞代码片段截取功能
* 支持漏洞位置行的高亮显示功能
* 支持漏洞关键信息的取证功能

1.6 扫描节点监控管理
^^^^^^^^^^^^^^^^^^^^^^^

* 支持扫描节点的状态监控
* 支持软件升级包在线打包、版本发布
* 支持软件升级包的历史记录自动生成与历史记录查看
* 使用 RSA 非对称加密方式，对节点间传输内容进行加密

1.7 扫描引擎特点
^^^^^^^^^^^^^^^^^^^

* 完成 65% 的代码单元测试覆盖率，保证程序代码健壮
* 完成 SonarScanner、RuleScanner、PluginScanner 引擎的功能测试，来保证程序正常运行
* 提供命令行接口，并可通过命令行接口对线上项目、本地项目进行扫描
* 支持软件升级包的自动升级与规则热加载
* 支持扫描任务失败时的日志回传功能
* 支持命令行下工具自检
* 支持 Docker 部署

----

2. 系统设计
-------------------

.. image:: https://camo.githubusercontent.com/a70248635af08eca214ec28b589ae7526fa0f940/68747470733a2f2f736565636f64652d61756469742e72656164746865646f63732e696f2f656e2f6c61746573742f5f696d616765732f696d67312e706e67


2.1 存储层
^^^^^^^^^^^^^

存储服务主要用于对扫描任务的日志、扫描结果、离线项目 zip 包、加密升级包进行存储，其形式可为 FTP、AWS 或其他云存储服务（由于测试环境有限目前只支持 FTP）。

2.2 Audit 服务端
^^^^^^^^^^^^^^^^^^^^

Audit 服务端是 UI 前台系统，用于管理 SeeCode Audit 中的整体功能，其中包括 API 接口服务、项目管理、任务管理、引擎管理、节点管理、系统管理等功能。

2.3 中间件层
^^^^^^^^^^^^^^^

在生产环境下可使用 Memcached 做为缓存，使用 RabbitMQ 做为消息队列；测试与开发环境可以使用 Redis 代替以上服务。

2.4 Scan 扫描端
^^^^^^^^^^^^^^^^^^^

使用 seecode-scanner 作为扫描节点，并可水平扩展，详细参考请查看：https://seecode-scanner.readthedocs.io/en/latest/

----

3. 部署说明
------------

3.1 开发/测试环境
^^^^^^^^^^^^^^^^^^^^

* Python3 + Django2
* 数据库：MySQL
* 中间件：Redis、FTP

.. Note::

  搭建系统前请确保 MySQL、Redis、FTP 等服务已安装并启动。


**依赖安装**

.. code-block:: console

   $ # 使用 virtualenv
   $ virtualenv . && source bin/activate
   $ pip isntall -r requirements/dev.txt
   $ # 安装 seecode-scanner
   $ pip install https://github.com/seecode-audit/seecode-scanner/archive/1.0.0.zip


**系统搭建**

.. code-block:: console

   $ # 下载 seecode-audit 代码
   $ git clone git@github.com:seecode-audit/seecode-audit.git


创建 seecode_db_ce 数据库， 执行 extras/db/seecode_db_ce_struct.sql、 extras/db/seecode_db_ce_data.sql 脚本：

.. code-block:: console

   $ create database seecode_db_ce default character set utf8mb4 collate utf8mb4_unicode_ci;


**启动服务**


运行 Web 服务，成功后访问 http://127.0.0.1:8080, 账号/密码 ``root/1qaz!QAZ`` ：

.. code-block:: console

   $ make runserver

启动 GitLab 同步服务：

.. code-block:: console

   $ celery -A seecode.celeryctl.celery_app beat -l info -Q gitlab


3.2 生产环境部署
^^^^^^^^^^^^^^^^^^^^^^^

* Python3 + Django2 + CentOS 7
* 数据库：MySQL 集群
* 中间件：Memcached、RabbitMQ、FTP/AWS/其他云存储


.. Note::

  搭建系统前请确保 Nginx、MySQL、Memcached、RabbitMQ、FTP 等服务已安装并启动。

**依赖安装**

创建 seecode 账号

.. code-block:: console

   $ sudo useradd -m -s /bin/bash seecode && passwd seecode

切换 seecode 账号，开始搭建系统

.. code-block:: console

   $ # 创建部署目录
   $ sudo mkdir -p /usr/local/seecode && cd /usr/local/seecode
   $ # 设置部署目录权限
   $ sudo chown seecode:seecode /usr/local/seecode
   $ # 拉取线上代码
   $ git clone git@github.com:seecode-audit/seecode-audit.git && cd seecode-audit
   $ # 安装依赖
   $ pip isntall -r requirements/prod.txt
   $ # 安装 seecode-scanner
   $ pip install https://github.com/seecode-audit/seecode-scanner/archive/1.0.0.zip

**配置系统**

添加 nginx 配置

.. code-block:: console

   $ sudo cp extras/conf/nginx.conf /etc/nginx/conf.d/seecode.conf

添加 supervisord 配置

.. code-block:: console

   $ sudo cp extras/conf/supervisord.conf /etc/supervisord.conf

添加 seecode 配置

.. code-block:: console

   $ sudo cp extras/conf/seecode.yml /etc/seecode.yml

修改 RSA 的公钥与私钥：

.. code-block:: console

   $ vim seecode/libs/core/rsaencrypt.py

**初始化系统**

创建 seecode_db_ce 数据库， 执行 extras/db/seecode_db_ce_struct.sql、 extras/db/seecode_db_ce_data.sql 脚本：

.. code-block:: console

   $ create database seecode_db_ce default character set utf8mb4 collate utf8mb4_unicode_ci;

登陆系统，配置 GitLab、配置 SonarQube。

**运行系统**

.. code-block:: console

   $ supervisord -c /etc/supervisord.conf >/dev/null 2>&1 &

----

捐赠
--------

* BTC 地址：18F4VFDX2MCEXod7zjUF8NepUdAspEcJR8
* ETH 地址：0xB3Bc55F4AAa8E87D3675B547e31d3eEbb585175c
* HT 地址：0x952b4cd9f18126987fdbfab55e1ea72c5ae72e16

----