# coding: utf-8

import os
import multiprocessing

bind = "{0}:{1}".format(
    os.getenv("SEECODE_HOST", '127.0.0.1'),
    os.getenv("SEECODE_PORT", 1768),
)
errorlog = '/var/log/seecode/gunicorn.error.log'
accesslog = '/var/log/seecode/gunicorn.access.log'
#loglevel = 'debug'
proc_name = 'seecode'
#chdir = '/opt/seecode/bin'
timeout = 30
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
