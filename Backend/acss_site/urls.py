"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls.conf import include

from acss_app import admin_urls
from acss_app import user_urls
from acss_app import generic_urls
from acss_app import charge_urls
from acss_app import queue_urls


urlpatterns = [
    path('admin/', include(admin_urls)),
    path('user/', include(user_urls)),
    path('charging/', include(charge_urls)),
    path('queue/', include(queue_urls)),
    path('', include(generic_urls)),
]
