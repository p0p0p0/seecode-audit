
========================
生产环境
========================


1. 安装
========================

* 下载程序

通过 https://github.com/seecode-audit/seecode-audit/releases 下载最新版本。
解压安装的 zip 包，这里安装在 /usr/local/seecode-audit/ 路径下。

.. code-block:: console

   $ sudo unzip seecode-audit.zip -d /usr/local/seecode-audit/

.. install :

* 安装依赖包

.. code-block:: console

   $ pip isntall -r requirements/dev.txt
   $ pip install https://github.com/seecode-audit/seecode-scanner/archive/1.0.0.zip


----

2. 配置
========================

2.1 配置 seecode.yml
------------------------------

编辑 /etc/seecode.yml 文件，请确认所有环境变量中都使用 ``DJANGO_SETTINGS_MODULE=seecode.settings.prod``。

.. code-block:: yaml

	mysql:
	  default:
	    host: 10.168.1.2
	    port: 3306
	    username: "seecode_db"
	    password: "*****************"
	    database: "seecode_db_ce"
	  slave:
	    host: 10.168.1.3
	    port: 3306
	    username: "seecode_db"
	    password: "*****************"
	    database: "seecode_db_ce"
	
	redis:
	  host: 10.168.1.1
	  port: 6379
	  db: 1
	  password: "*****************"
	
	memcached:
	  host:
	    172.19.26.1:11211
	    172.19.26.2:11211
	    172.19.26.3:11211
	    172.19.26.4:11211
	  username: seecode
	  password: "*****************"
	
	celery:
	  celery_broker_url: ""
	
	env:
	  SEECODE_CELERY_BROKER_URL: "redis://:*****************@10.168.1.4:6379/8"
	  SEECODE_C_FORCE_ROOT: False


* 数据库
^^^^^^^^^

数据库默认使用 MySQL，部署方式读写分离。default 节点用于写入，slave 节点用于读取。

* 缓存
^^^^^^^^

  - redis

   使用 Redis 用于缓存。

  - memcached

   使用 emcached 用于缓存。

* Celery
^^^^^^^^^^

  - celery

   该节点为中的 celery 配置，用于 seecode-audit 的 Gitlab 的队列。

  - env

   用于设置 eecode Audit 的环境变量，默认设置了 seecode-scanner 使用的环境变量。

2.2 配置 Nginx
------------------------------

创建 /etc/nginx/conf.d/seecode.conf 文件，需要注意 server_name、static、proxy_pass 的正确设置。

.. code-block:: console

   server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  seecode-audit.com;  # domain

        location /static {
            alias /usr/local/seecode-audit/seecode/templates/static;
        }

        location / {
            proxy_pass http://127.0.0.1:1768;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_connect_timeout 75s;
            proxy_read_timeout 600s;

        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
   }


2.3  配置 gunicorn
------------------------------

编辑 seecode/gunicorn.conf.py 文件内容。 配置 /etc/supervisord.conf 设置， 注意 /etc/directory 与 /usr/local/bin/gunicorn 中的路径是否设置正确。

.. code-block:: console

   [program:gunicorn]
   directory=/usr/local/seecode-audit
   environment=DJANGO_SETTINGS_MODULE=seecode.settings.prod
   command=/usr/local/bin/gunicorn seecode.wsgi:application -c /usr/local/seecode-audit/seecode/gunicorn.conf
   .py --timeout 600
   autorestart=true


2.4 配置 Celery
------------------------------

注意 directory 与 /usr/local/bin/celery 中的路径是否正确

.. code-block:: console

   [program:celery-beat]
   directory=/usr/local/seecode-audit
   environment=DJANGO_SETTINGS_MODULE=seecode.settings.prod
   command=/usr/local/bin/celery -A seecode.celeryctl.celery_app beat -l info -Q gitlab
   autorestart=true

----

3. 运行
========================

确保 supervisord.conf 中的配置项与服务器配置的路径一致：


.. code-block:: bash
 
   $ supervisord -c /etc/supervisord.conf >/dev/null 2>&1 &