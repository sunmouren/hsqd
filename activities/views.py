from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Activity


class ActivityList(View):
    """
    活动列表，加入活动
    """
    def get(self, request):
        current_page = 'activity-list'
        activities = Activity.objects.all()
        return render(request, 'activities/activity-list.html', {
            'activities': activities,
            'current_page': current_page,
        })

    def post(self, request):
        if request.is_ajax():
            activity_id = request.POST.get('acid', None)
            action = request.POST.get('action', None)

            if activity_id and action:
                try:
                    activity = Activity.objects.get(id=int(activity_id))
                    if action == 'join':
                        activity.guests.add(request.user)
                    else:
                        activity.guests.remove(request.user)
                    return JsonResponse({'msg': 'ok'})
                except Activity.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class ActivityDetail(View):
    """
    活动详情
    """
    def get(self, request, aid):
        activity = get_object_or_404(Activity, id=int(aid))
        return render(request, 'activities/activity-detail.html', {'activity': activity})

    def post(self, request):
        if request.is_ajax():
            aid = request.POST.get('aid')
            action = request.POST.get('action')
            if aid and action:
                try:
                    activity = Activity.objects.get(id=int(aid))
                    if action == 'activate':
                        activity.is_active = True
                    else:
                        activity.is_active = False
                        activity.save()
                    return JsonResponse({'msg': 'ok'})
                except Activity.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class ActivityActivate(LoginRequiredMixin, View):
    """
    是否开启签到
    """
    def post(self, request):
        if request.is_ajax():
            aid = request.POST.get('aid', None)
            action = request.POST.get('action', None)
            if aid and action:
                try:
                    activity = Activity.objects.get(id=int(aid))
                    if action == 'activate':
                        activity.is_active = True
                        self.sign_index_action(action)
                    else:
                        activity.is_active = False

                    activity.save()
                    return JsonResponse({'msg': 'ok'})
                except Activity.DoesNotExist:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})

    def sign_index_action(self, action):
        pass
