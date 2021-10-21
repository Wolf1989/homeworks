""" app URL Configuration """
from django.urls import path

from app.views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('current_time/', time_view, name='time'),
    path('workdir/', workdir_view, name='workdir'),
]
