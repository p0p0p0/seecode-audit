# coding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import update_last_login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@ensure_csrf_cookie
def login(request):
    """
    :param request:
    :return:
    """
    username = request.POST.get('username', None)
    userpwd = request.POST.get('userpwd', None)
    next_url = request.GET.get('next', None)

    if username and userpwd:
        user = authenticate(username=username, password=userpwd)

        if user is not None:
            django_login(request, user)
            update_last_login(request, user)
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect("/")
        else:
            return render(request, 'auth/login.html', {'failure': True, 'next_url': 'next={0}'.format(next_url)})

        if not user.is_active:
            return render(
                request, 'auth/login.html',
                {'failure': True,
                 'type': 'is_active',
                 'next_url': 'next={0}'.format(next_url)})

    else:
        return render(
            request=request,
            template_name='auth/login.html',
            context={'next_url': 'next={0}'.format(next_url)}
        )


def logout(request):
    django_logout(request)
    # views.logout(request)
    return HttpResponseRedirect("/login/")


def error_403(request):
    return render(
        request,
        '403.html',
    )
