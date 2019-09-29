
from django.urls import path

from seecode.apps.tactic.views import rule
from seecode.apps.tactic.views import kb
from seecode.apps.tactic.views import kb_cate
from seecode.apps.tactic.views import engine


urlpatterns = [
    path(r'rule/', rule.index),
    path(r'rule/<int:tactic_id>/', rule.show),
    path(r'rule/verify/', rule.verify_regex),
    path(r'rule/batch/', rule.batch),
    path(r'rule/exists/', rule.exists),

    # kb
    path(r'kb/', kb.index),
    path(r'kb/<int:vuln_id>/', kb.show),
    path(r'kb/upload/', kb.upload),
    path(r'kb/search/', kb.search),
    path(r'kb/edit/', kb.show),

    path(r'kb/cate/', kb_cate.index),
    path(r'kb/cate/<int:cate_id>/', kb_cate.show),
    path(r'kb/origin/', kb_cate.origin_index),

    # engine
    path(r'engine/', engine.index),
    path(r'engine/<int:engine_id>/', engine.edit),

]
