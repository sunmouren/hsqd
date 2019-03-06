# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/2/27 20:33
@desc: 
"""

from django.urls import path

from .views import PostList, AddPost, PostDetail, AddComment

app_name = 'posts'


urlpatterns = [
    path('list/', PostList.as_view(), name='post-list'),
    path('add/', AddPost.as_view(), name='post-add'),
    path('detail/<int:pid>/', PostDetail.as_view(), name='post-detail'),
    path('comment/add/', AddComment.as_view()),
]