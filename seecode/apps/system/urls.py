
from django.urls import path

from seecode.apps.system.views import settings
from seecode.apps.system.views import account
from seecode.apps.system.views import group
from seecode.apps.system.views import permission
from seecode.apps.system.views import syslog
from seecode.apps.system.views import service
from seecode.apps.system.views import sched
from seecode.apps.system.views import lang


urlpatterns = [

    # settings
    path(r'settings/', settings.index),
    path(r'clear/', settings.clear_cached),


    # account
    path(r'account/', account.index),
    path(r'account/token/', account.token),
    path(r'account/<int:user_id>/', account.show),
    path(r'account/search/', account.search),
    path(r'group/', group.index),
    path(r'group/<int:group_id>/', group.show),
    path(r'group/member/<int:group_id>/', group.member_index),
    path(r'account/perm/', permission.index),
    path(r'account/perm/<int:perm_id>/', permission.show),
    path(r'account/perm/batch/', permission.delete),

    # syslog
    path(r'log/', syslog.index),
    path(r'log/<int:syslog_id>', syslog.show),

    path(r'service/', service.index),
    path(r'service/<int:s_id>/', service.show),
    path(r'service/sched/', sched.index),

    # lang
    path(r'lang/', lang.index),

]
