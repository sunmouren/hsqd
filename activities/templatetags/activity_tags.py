# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/2/27 16:36
@desc: 
"""

from django import template


register = template.Library()


@register.simple_tag
def is_joined_activity(user, activity):
    """
    判断用户是否在加入活动
    :param user:
    :param activity:
    :return:
    """
    return user in activity.guests.all() if user.is_authenticated else False


@register.simple_tag
def is_signed_activity(user, activity):
    """
    判断用户签到
    :param user:
    :param activity:
    :return:
    """
    return user in activity.signed_in_users.all() if user.is_authenticated else False
