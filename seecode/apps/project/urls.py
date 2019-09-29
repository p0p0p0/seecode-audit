# coding: utf-8

from django.urls import path

from seecode.apps.project.views import group
from seecode.apps.project.views import item as project
from seecode.apps.project.views import member
from seecode.apps.project.views import component
from seecode.apps.project.views import app

urlpatterns = [

    # group
    path('group/', group.index),
    path('group/<int:group_id>/', group.show),
    path('group/batch/', group.batch),
    path('group/search/', group.search),
    path('group/exists/', group.exists),

    # project
    path('', project.index),
    path('<int:project_id>/', project.show),
    path('batch/', project.batch),

    # app
    path('app/', app.index),
    path('app/search/', app.search),
    path('app/batch/', app.batch),
    path('app/<int:app_id>/', app.show),

    # member
    path('member/', member.index),

    # component
    path('component/', component.index),
    path('component/export/', component.export),


]
