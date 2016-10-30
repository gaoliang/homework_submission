"""homework_submisson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from submission_system.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'index/', index_view, name='index'),
    url(r'^accounts/', include('auth_system.urls')),
    url(r'submission-detail/$', add_submission, name='_submission_detail'),
    url(r'add-submission/$', add_submission, name='_add_submission'),
    url(r'homework-detail/$', homework_detail, name="_homework_detail"),
    url(r'list-homework/(?P<courser_name_en>[a-zA-Z0-9#+_]+)/', list_homework, name='list_homework'),
    url(r'add-homework/(?P<courser_name_en>[a-zA-Z0-9#+_]+)/', add_homework, name='add_homework'),
    url(r'get-homework-list/(?P<courser_name_en>[a-zA-Z0-9#+_]+)/', get_homework_list, name='get_homework_list'),
    url(r'homework-detail/(?P<homework_id>\d+)/', homework_detail, name='homework_detail'),
    url(r'get-finished/(?P<homework_id>\d+)/', get_finished, name='get_finished'),
    url(r'add-submission/(?P<homework_id>\d+)/', add_submission, name='add_submission'),
    url(r'submission-detail/(?P<submission_id>\d+)', submission_detail, name='submission_detail'),
    url(r'list_my_submissions', list_my_submissions, name='list_my_submissions'),
    url(r'get_my_submissions', get_my_submissions, name="get_my_submissions"),
    url(r'^$', index_view)
]
