# -*- coding: utf-8 -*-
"""evotor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    url(r'^user/create/$', csrf_exempt(views.UserCreateView.as_view()), name="create"),
    url(r'^user/verify/$', csrf_exempt(views.UserVerifyView.as_view()), name="verify"),
    url(r'^user/token/$', csrf_exempt(views.UserTokenView.as_view()), name="token"),

    url(r'^subscription/event/$', csrf_exempt(views.SubscriptionEventView.as_view()), name="subscriptionEvent"),
    url(r'^installation/event/$', csrf_exempt(views.InstallationEventView.as_view()), name="installationEvent"),


    # Урлы для работы фронтэнда
    url(r'^stores/$', csrf_exempt(views.StoresListView.as_view()), name="stores"),

    #url(r'^stores/$', views.StoreList.as_view()),
    #url(r'^stores/(?P<uuid>[0-9A-Fa-f-]+/$)', views.StoreDetail.as_view()),
    # url('', views.UserList.as_view()),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# urlpatterns += router.urls
