"""admin URL Configuration

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

from django.conf.urls import url,include
from app01 import views

app_name = 'app01'

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^host_list/', views.host_list),
    url(r'^info_manage/', views.info_manage),
    url(r'^hostedit-(?P<nid>\d+)/', views.host_edit),
    url(r'^init/', views.init),
    url(r'^introduce/', views.introduce),
    url(r'^logout/', views.logout),
    url(r'^hostdel-(?P<nid>\d+)/', views.host_del),
    url(r'^infodel_user-(?P<id>\d+)/', views.info_user_del),
    url(r'^infodel_area-(?P<id>\d+)/', views.info_area_del),
    url(r'^infodel_business-(?P<id>\d+)/', views.info_business_del),
    url(r'^infoedit_user-(?P<id>\d+)/',views.info_user_edit.as_view()),
    url(r'^infoedit_area-(?P<id>\d+)/',views.info_area_edit.as_view()),
    url(r'^infoedit_business-(?P<id>\d+)/',views.info_business_edit.as_view()),
    url(r'^hostadd/', views.host_add),
    url(r'^infouseradd/', views.info_user_add.as_view()),
    url(r'^infoareaadd/', views.info_area_add.as_view()),
    url(r'^infobusinessadd/', views.info_business_add.as_view()),
]