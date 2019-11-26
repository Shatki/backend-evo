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
# from graphene_django.views import GraphQLView

from . import views

urlpatterns = [
    # Урлы для облака Эвотор
    url(r'^user/create/$', csrf_exempt(views.UserCreateView.as_view()), name="create"),
    url(r'^user/verify/$', csrf_exempt(views.UserVerifyView.as_view()), name="verify"),
    url(r'^user/token/$', csrf_exempt(views.UserTokenView.as_view()), name="token"),

    url(r'^subscription/event/$', csrf_exempt(views.SubscriptionEventView.as_view()), name="subscriptionEvent"),
    url(r'^installation/event/$', csrf_exempt(views.InstallationEventView.as_view()), name="installationEvent"),

    # Урлы для работы фронтэнда
    # Авторизация пользователя к бекенду

    # Запрос всех магазинов пользователя, по токену и user_id
    # https://api.evotorservice.ru/a06c4306-732d-4914-9543-a588af06c683/stores
    url(r'^stores/$',
        csrf_exempt(views.StoresListView.as_view()), name="stores"),

    # Запрос всех товаров, по токену и user_id
    # https://api.evotorservice.ru/a06c4306-732d-4914-9543-a588af06c683/store/20180507-447F-40C1-8081-52D4B03CD7AB/products/
    url(r'^store/(?P<store_uuid>[0-9A-Fa-f-]+)/products/$',
        csrf_exempt(views.ProductsListView.as_view()), name="products"),


    #url(r'^user/(?P<user_id>[0-9-]+)/stores/(?P<token>[0-9A-Za-z-]+)$', views.StoreList.as_view()),
    #url(r'^stores/(?P<uuid>[0-9A-Fa-f-]+/$)', views.StoreDetail.as_view()),
    # url('', views.UserList.as_view()),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # GraphQL API
    # url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
]

# urlpatterns += router.urls
