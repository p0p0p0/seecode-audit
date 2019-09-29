
========================
开发测试
========================

此方式用于开发与测试时使用。


1. 安装
===============

* 使用 git 下载源代码

.. code-block:: console

   $ git clone git@github.com:seecode-audit/seecode-scanner.git


* 使用 virtualenv 安装依赖

.. code-block:: console

   $ virtualenv . && source bin/activate
   $ pip isntall -r requirements/dev.txt
   $ pip install https://github.com/seecode-audit/seecode-scanner/archive/1.0.0.zip



2. 配置
===============

* 配置数据库， 修改 seecode/settings/dev.py 文件


**MySQL**

.. code-block:: python

   DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seecode_db_ce',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
      }
   }

**Sqlite3**

.. code-block:: python

   DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'seecode_db_ce.db'),
      }
   }


* 配置 Redis

**缓存**： 修改 seecode/settings/dev.py 文件

.. code-block:: python

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "KEY_PREFIX": "seecode_ce",
            "LOCATION": "redis://127.0.0.1:6379/7",  # 修改
            "OPTIONS": {
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": "",
                "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
                "SOCKET_TIMEOUT": 5,  # in seconds
                "PICKLE_VERSION": -1  # Use the latest protocol version
            }
        }
    }


**服务端 Celery 队列**： 修改 seecode/settings/dev.py 文件

.. code-block:: python

   CELERY_BROKER_URL = "redis://127.0.0.1:6379/7"


**扫描端（seecode-scanner）Celery 队列**： 修改 Makefile 文件

.. code-block:: bash

    runserver:
        export SEECODE_CELERY_BROKER_URL=redis://127.0.0.1:6379/2 && \
        export SEECODE_C_FORCE_ROOT=False && \
        export DJANGO_SETTINGS_MODULE=seecode.settings.dev && python manage.py runserver 0.0.0.0:8080

* 配置 seecode/wsgi.py 文件， 'seecode.settings.prod' 修改为 'seecode.settings.dev'。

.. code-block:: bash

    $ os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seecode.settings.dev')

* 配置 seecode/celeryctl.py 文件， 'seecode.settings.prod' 修改为 'seecode.settings.dev'。

.. code-block:: bash

    $ os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seecode.settings.dev')

3. 运行
===============

* Web 启动

.. code-block:: bash

   $ make runserver
    export SEECODE_CELERY_BROKER_URL=redis://127.0.0.1:6379/2 && \
            export SEECODE_C_FORCE_ROOT=False && \
            export DJANGO_SETTINGS_MODULE=seecode.settings.dev && python manage.py runserver 0.0.0.0:8080
    Watching for file changes with StatReloader
    Performing system checks...
    
    System check identified no issues (0 silenced).
    September 21, 2019 - 11:24:31
    Django version 2.2.5, using settings 'seecode.settings.dev'
    Starting development server at http://0.0.0.0:8080/
    Quit the server with CONTROL-C.


* Gitlab 同步

.. code-block:: bash

   $ celery -A seecode.celeryctl.celery_app -b -l info -Q gitlab


4. 测试
===============


* 执行 Gitlab 同步

.. code-block:: bash

   $ make unit
