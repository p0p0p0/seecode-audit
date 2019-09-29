# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache


class PermWrapper(object):
    def __init__(self, user):
        self.user = user
        self.group = None
        self.perms = {}
        self.perm_list = []

        if self.user.groups.all():
            group = self.user.groups.all()[0]
            for perm in group.permissions.all():
                app_label = perm.content_type.app_label
                perm_name = perm.codename
                if app_label not in self.perms:
                    self.perms[app_label] = {}
                self.perms[app_label][perm_name] = True
                self.perm_list.append('{0}.{1}'.format(app_label, perm_name))

    def __getitem__(self, app_label):
        return self.perms[app_label]
