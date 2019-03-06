# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/2/26 21:10
@desc: 
"""

from django.urls import path

from .views import UserRegister, UserLogout, UserLogin, NoLogin, UserHome

app_name = 'users'


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('no/login/', NoLogin.as_view()),
    path('home/<int:uid>/', UserHome.as_view(), name='user-home'),
]