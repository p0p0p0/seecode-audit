# coding: utf-8

from django.urls import path

from seecode.apps.node.views import host
from seecode.apps.node.views import service
from seecode.apps.node.views import upgrade


urlpatterns = [
    path(r'', host.index),
    path(r'service/', service.index),
    path(r'upgrade/', upgrade.index),
    path(r'upgrade/<int:upgrade_id>/', upgrade.show),
    path(r'upgrade/download/<int:upgrade_id>/', upgrade.download),

]
