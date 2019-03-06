from django.db import models
from django.conf import settings
from django.urls import reverse


class Activity(models.Model):
    """
    活动表
    """
    title = models.CharField(max_length=100, verbose_name='活动标题')
    address = models.CharField(max_length=50, verbose_name='活动地址')
    start_time = models.CharField(max_length=50, verbose_name='开始时间', blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name='是否开启签到')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='activities_creator', verbose_name='创建者')
    guests = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                    related_name='activities_guest', verbose_name='嘉宾')
    signed_in_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                             related_name='activities_signed_in', verbose_name='已签到嘉宾')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def get_absolute_url(self):
        return reverse('activities:activity-detail', args=[self.id])

    def __str__(self):
        return self.title





