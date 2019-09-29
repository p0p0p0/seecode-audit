# -*- coding: utf-8 -*-

import datetime

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    health = 100



    return render(request, 'system/home.html', {
            'nav': 'dashboard',

        })
