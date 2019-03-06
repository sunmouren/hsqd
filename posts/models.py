from django.db import models
from django.conf import settings
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class PublishedManager(models.Manager):
    """
    已激活文章的管理器
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(is_active=True)


class Post(models.Model):
    """
    文章表
    """
    title = models.CharField(max_length=120, verbose_name='标题')
    body = models.TextField(verbose_name='内容')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='posts', verbose_name='作者')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 默认的管理器
    objects = models.Manager()
    # 自定义的管理器
    published = PublishedManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-created', )

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=[self.id])

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    """
    文章评论
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                            related_name='replies', verbose_name='父级评论')
    content = models.TextField(verbose_name='评论内容', default=None)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments',
                                       blank=True)
    like_number = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='评论时间')

    class MPTTMeta:
        order_insertion_by = ('created', )

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.parent is not None:
            return '{0} 回复 {1}'.format(self.user.username, self.parent.user.username)
        else:
            return '{0} 评论了 {1}'.format(self.user.username, self.video)
