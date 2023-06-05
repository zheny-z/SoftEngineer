"""充电相关接口路由"""
from django.urls import path

import acss_app.controller.user_controller as user_controller


urlpatterns = [
    path('request', user_controller.submit_charging_request),
    path('query_order_detail', user_controller.query_orders_api),
    path('submit', user_controller.end_charging_request),
]