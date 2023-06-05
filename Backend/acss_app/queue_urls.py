"""排队调度相关接口路由"""
from django.urls import path

import acss_app.controller.user_controller as user_controller


urlpatterns = [
    path('edit_charging_request', user_controller.edit_charging_request),
    path('preview_queue', user_controller.preview_queue_api),
]
