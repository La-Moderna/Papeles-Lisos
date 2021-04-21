"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from importlib import import_module

from django.contrib import admin
from django.urls import include, path, re_path

from utils.routers import DefaultRouter

from app.settings import LOCAL_APPS

router = DefaultRouter(trailing_slash=False)


def autodiscover():
    "Search for api.py files in the local apps"
    for app in LOCAL_APPS:
        try:
            import_module('.'.join((app, 'api')))
        except ImportError as e:
            if e.msg != "No module named '{0}.api'".format(app):
                print(e.msg)


autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include(router.urls))
]
