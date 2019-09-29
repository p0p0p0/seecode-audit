# -*- coding: utf-8 -*-
from django.urls import path

from seecode.apps.scan.views import task
from seecode.apps.scan.views import issue
from seecode.apps.scan.views import group
from seecode.apps.scan.views import scan_template
from seecode.apps.scan.views import scan_template_item

urlpatterns = [

    # settings
    path(r'group/', group.index),
    path(r'group/<int:group_id>/', group.show),
    path(r'group/search/', group.search),
    path(r'group/batch/', group.batch),

    path(r'task/', task.index),
    path(r'task/<int:task_id>/', task.show),
    path(r'log/<int:task_id>/', task.download_log),
    path(r'task/batch/', task.batch),
    path(r'<int:task_id>/issue/', issue.index),
    path(r'issue/', issue.index),
    path(r'issue/<int:issue_id>/', issue.show),

    # scan template
    path(r'template/', scan_template.index),
    path(r'template/<int:profile_id>/', scan_template.show),
    path(r'template/tactic/', scan_template.tactic),
    
    # scan template items
    path(r'template/<int:template_id>/tactics/', scan_template_item.index),

]
