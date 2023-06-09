"""管理员相关接口路由"""
from django.urls import path

from acss_app.controller.admin_controller import query_all_piles_stat_api, query_queue_api, query_report_api, update_pile_status_api


urlpatterns = [
    path('query-all-piles_stat', query_all_piles_stat_api),
    path('update-pile', update_pile_status_api),
    path('query-report', query_report_api),
    path('query-queue', query_queue_api)
]
