
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

``SeeCode Audit`` 是一套代码审计的 UI 前端框架系统，该系统需要结合 `seecode-scanner <https://github.com/seecode-audit/seecode-scanner>`_
工具一起使用。 ``SeeCode Audit`` 是使用 Python3 + Django2 + MySQL + Redis/Memcached + Redis/RabbitMQ 技术搭建。


**1. 系统设计：**
-------------------

.. image:: https://seecode-audit.readthedocs.io/en/latest/_images/img1.png


1.1 存储层
^^^^^^^^^^^

存储服务主要用于对扫描任务的日志、扫描结果、离线项目 zip 包、加密升级包进行存储，其形式可为FTP、AWS或其他云存储服务（由于测试环境有限目前只支持FTP）。

1.2 Audit 服务端
^^^^^^^^^^^^^^^^^^^^^^

Audit 服务端是 UI 前台系统，用于管理 SeeCode Audit 中的整体功能，其中包括 API 接口服务、项目管理、任务管理、引擎管理、节点管理、系统管理等功能。

1.3 中间件层
^^^^^^^^^^^^^^^^^^^^^^

中间使用到 Memcached 缓存、RabbitMQ 队列，测试与开发环境可以使用 Redis 代替以上服务。

1.4 Scan 扫描端
^^^^^^^^^^^^^^^^^^^^^^

seecode-scanner 扫描节点，可水平扩展。详细参考：https://seecode-scanner.readthedocs.io/en/latest/


**2. 功能特点：**
-------------------

.. login :

- **多种登录认证方式**

  * 支持 SSO、Django authentication 方式认证

.. project :

- **项目与应用快捷管理**

  * 支持线上（GitLab）项目同步与管理，支持项目时间轴事件查看
  * 支持项目应用概念，提供应用创建、编辑、健康度与风险分析功能
  * 支持 zip 源码包的项目类型扫描

.. template :

- **支持扫描模板自定义**

  * 支持自定义扫描模板，并为扫描模板添加检测规则、添加扫描引擎

.. rule :

- **支持扫描规则与插件管理**

  * 支持自定义规则添加，规则检测类型：目录、文件、内容、组件等方式
  * 支持 Python 脚本的插件功能

.. scan :

- **扫描节点监控管理**

  * 提供采集 API 接口用于接受扫描端的信息采集
  * 通信内容使用 RSA 进行加密


3. 部署说明
------------

3.1 开发/测试环境
^^^^^^^^^^^^^^^^^^^^^^^^

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

捐赠
--------

* BTC 地址：18F4VFDX2MCEXod7zjUF8NepUdAspEcJR8
* ETH 地址：0xB3Bc55F4AAa8E87D3675B547e31d3eEbb585175c
