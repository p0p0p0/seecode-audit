"""seecode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static

from cas import views

try:
    import debug_toolbar
except ImportError:
    pass

import seecode.apps.authenticate.views.auth as authview
import seecode.apps.system.views.home as home

urlpatterns = [
        path('', home.index),
]

if settings.ENABLE_CAS_SSO:
    urlpatterns += [
        path(r'login/', views.login, name='login'),
        path(r'logout/', views.logout, name='logout'),
    ]
else:
    urlpatterns += [
        path('login/', authview.login),
        path('logout/', authview.logout),
    ]

urlpatterns += [
    url(r'^api/v2/', include('seecode.apps.api.v2.urls'))
]

urlpatterns += [
    path('sys/', include('seecode.apps.system.urls'))
]

urlpatterns += [
    path('node/', include('seecode.apps.node.urls'))
]

urlpatterns += [
    path('project/', include('seecode.apps.project.urls'))
]

urlpatterns += [
    path('scan/', include('seecode.apps.scan.urls'))
]

urlpatterns += [
    path('tactic/', include('seecode.apps.tactic.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)
    try:
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except:
        pass

