# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import app_view, register_user, exist_app_view, fill_app
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('newapp/', app_view, name="newapp"),
    path('existapp', exist_app_view, name="existapp"),
    path('fillapp', fill_app, name="fillapp"),
    path("logout/", LogoutView.as_view(), name="logout")
]
