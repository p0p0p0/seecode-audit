# coding: utf-8

from __future__ import unicode_literals

import os
import django.conf

from celery import Celery

celery_app = Celery('seecode')

from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seecode.settings.prod')
django.setup()


celery_app.conf.update(
    BROKER_URL=settings.CELERY_BROKER_URL,
    CELERY_TASK_SERIALIZER='pickle',
    CELERY_RESULT_SERIALIZER='pickle',
    CELERY_ACCEPT_CONTENT=['pickle'],
    CELERYD_POOL_RESTART=False,
    CELERY_ENABLE_UTC=False,
    CELERYD_MAX_TASKS_PER_CHILD=50,
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600 * 24 * 7},
    CELERY_IMPORTS=(
        'seecode.services.gitlab_sync',
    ),
    CELERY_ROUTES={
        'seecode.services.gitlab_sync.start': {'queue': 'gitlab'},
    }
)
