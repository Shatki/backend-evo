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
from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='Users')
router.register(r'user/create', views.UserViewSet, basename='UserCreate')
router.register(r'user/verify', views.UserViewSet, basename='UserVerify')

router.register(r'installations', views.InstallationViewSet, basename='Installations')
router.register(r'installation/event', views.InstallationEventViewSet, basename='InstallationEvent')

router.register(r'subscriptions', views.SubscriptionViewSet, basename='Subscriptions')
router.register(r'subscription/event', views.SubscriptionEventViewSet, basename='SubscriptionEvent')

# router.register(r'products', views.ProductViewSet, basename='Product')
# router.register(r'groups', views.GroupViewSet)
router.register(r'stores', views.StoreViewSet, basename='Stores')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url('^users/', include('users.urls')),
    #url(r'^stores/$', views.StoreList.as_view()),
    #url(r'^stores/(?P<uuid>[0-9A-Fa-f-]+/$)', views.StoreDetail.as_view()),
    # url('', views.UserList.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url('^subscription/event', include('users.urls')),
]

urlpatterns += router.urls
