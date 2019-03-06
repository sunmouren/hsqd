from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import View

from .models import UserProfile


class UserRegister(View):
    """
    注册
    """
    def post(self, request):
        if request.is_ajax():
            email = request.POST.get('email', None)
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            if email and password1 and password2:
                username = email.split('@')[0]
                if UserProfile.objects.filter(username=username).exists():
                    return JsonResponse({'msg': 'exists'})
                if not password1 == password2:
                    return JsonResponse({'msg': 'mismatch'})
                new_user = UserProfile(username=username, email=email)
                new_user.password = make_password(password2)
                new_user.save()
                return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'ko'})


class CustomBackend(ModelBackend):
    """
    增加邮箱登录
    继承ModelBackend类，覆盖authenticate方法, 增加邮箱认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用get是因为不希望用户存在两个, Q：使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 判断密码是否匹配时，django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有check_password(self, raw_password)方法
            if user.check_password(password):
                return user
        except BaseException as e:
            return None


class UserLogin(View):
    """
    登录
    """
    def post(self, request):
        if request.is_ajax():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'ko'})


class UserLogout(View):
    """
    注销
    """
    def get(self, request):
        logout(request)
        return JsonResponse({'msg': 'ok'})


class NoLogin(View):
    """
    未登录非法操作跳转视图
    """
    def get(self, request):
        return render(request, 'no-login.html')


class UserHome(View):
    """
    用户主页
    """
    def get(self, request, uid):
        user = get_object_or_404(UserProfile, id=int(uid))
        created_activities = user.activities_creator.all()
        join_activities = user.activities_guest.all()
        return render(request, 'users/user-home.html', {
            'user': user,
            'created_activities': created_activities,
            'join_activities': join_activities,
        })
