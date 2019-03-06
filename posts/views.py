from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import Post, Comment


# class PostList(ListView):
#     """
#     文章列表
#     """
#     model = Post
#     template_name = 'posts/post-list.html'

class PostList(View):
    """
    文章列表
    """
    def get(self, request):
        current_page = 'post-list'
        posts = Post.published.all()
        return render(request, 'posts/post-list.html', {
            'posts': posts,
            'current_page': current_page
        })


class AddPost(LoginRequiredMixin, View):
    """
    写文章
    """
    def get(self, request):
        return render(request, 'posts/add-post.html')

    def post(self, request):
        if request.is_ajax():
            title = request.POST.get('title', None)
            body = request.POST.get('body', None)
            if title and body:
                try:
                    new_post = Post(title=title, body=body)
                    new_post.user = request.user
                    new_post.save()
                    return JsonResponse({'msg': 'ok'})
                except BaseException:
                    return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ok'})


class PostDetail(View):
    """
    文章详情
    """
    def get(self, request, pid):
        post = get_object_or_404(Post, id=int(pid))
        comments = post.comment_set.order_by('-created')
        return render(request, 'posts/post-detail.html', {
            'post': post,
            'comments': comments
        })


class AddComment(LoginRequiredMixin, View):
    """
    添加问答
    """
    def post(self, request):
        pid = request.POST.get('pid', None)
        postid = request.POST.get('postid', None)
        content = request.POST.get('content', None)

        if request.is_ajax() and pid and postid and content:
            try:
                post = Post.objects.get(id=int(postid))
                parent = (Comment.objects.get(id=int(pid)) if int(pid) > 0 else None)
                new_comment = Comment(user=request.user, post=post, parent=parent, content=content)
                new_comment.save()
                cmt_html = render_comment_html(request=request, comment=new_comment)
                return JsonResponse({'msg': 'ok', 'cmt': cmt_html})
            except (Post.DoesNotExist, Comment.DoesNotExist, BaseException) as e:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


def render_comment_html(request, comment):
    """
    render comment to string html
    :param request:
    :param book:
    :param comment:
    :return:
    """
    cmt_html = render_to_string('posts/comment-item.html',
                                context={'comment': comment},
                                request=request)
    return cmt_html
