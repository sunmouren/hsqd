# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/2/27 15:51
@desc: 
"""

from django.urls import path

from .views import ActivityList, ActivityDetail, ActivityActivate

app_name = 'activities'

urlpatterns = [
    path('list/', ActivityList.as_view(), name='activity-list'),
    path('detail/<int:aid>/', ActivityDetail.as_view(), name='activity-detail'),
    path('detail/', ActivityDetail.as_view()),
    path('activate/', ActivityActivate.as_view()),
]