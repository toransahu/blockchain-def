#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Toran Sahu <toran.sahu@yahoo.com>
#
# Distributed under terms of the MIT license.

"""

"""

from .views import NotificationViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


app_name = 'common'

router = DefaultRouter()
router.register('notifications', NotificationViewSet, base_name='notifications')

urlpatterns = router.urls

