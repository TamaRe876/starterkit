from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Comment, Post
from .forms import CommentForm
from django.http import HttpResponseRedirect, JsonResponse
from users.models import Profile
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
import random
from blog.utils import is_ajax
from django.core.files.storage import FileSystemStorage
from notification.models import Notification
import re
from .forms import SupportMessageForm
from .models import SupportMessage
from django.contrib import messages

def terms(request):
    return render(request, 'blog/terms.html')


@login_required
def support(request):
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('support')

        admin_response = request.POST.get('admin_response')
        if admin_response and request.user.is_staff:
            message_id = request.POST.get('message_id')
            try:
                message = SupportMessage.objects.get(id=message_id)
                message.admin_response = admin_response
                message.responded = True
                message.save()
                message.success(request, 'Admin response sent successfully.')
            except SupportMessage.DoesNotExist:
                pass

            return redirect('support')
    else:
        form = SupportMessageForm()

    messages = SupportMessage.objects.filter(user=request.user).order_by('-timestamp')

    context = {
        'form': form,
        'messages': messages,
    }
    return render(request, 'blog/support.html', context)


def privacypolicy(request):
    return render(request, 'blog/privacypolicy.html')


def first(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/first.html', context)


""" Posts of following user profiles """


@login_required
def posts_of_following_profiles(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    qs = None
    for u in users:
        p = Profile.objects.get(user=u)
        p_posts = p.user.post_set.all()
        posts.append(p_posts)
    my_posts = profile.profile_posts()
    posts.append(my_posts)
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)

    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/feeds.html', {'profile': profile, 'posts': posts_list})


""" Post Like """


@login_required
def LikeView(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        notify = Notification.objects.filter(post=post, sender=request.user, notification_type=1)
        notify.delete()
    else:
        post.likes.add(request.user)
        liked = True
        notify = Notification(post=post, sender=request.user, user=post.author, notification_type=1)
        notify.save()

    context = {
        'post': post,
        'total_likes': post.total_likes(),
        'liked': liked,
    }

    if is_ajax(request=request):
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})


""" Post save """


@login_required
def SaveView(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    saved = False
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True

    context = {
        'post': post,
        'total_saves': post.total_saves(),
        'saved': saved,
    }

    if is_ajax(request=request):
        html = render_to_string('blog/save_section.html', context, request=request)
        return JsonResponse({'form': html})


""" Like post comments """


@login_required
def LikeCommentView(request):  # , id1, id2              id1=post.pk id2=reply.pk
    post = get_object_or_404(Comment, id=request.POST.get('id'))
    cliked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        cliked = False
    else:
        post.likes.add(request.user)
        cliked = True

    cpost = get_object_or_404(Post, id=request.POST.get('pid'))
    total_comments2 = cpost.comments.all().order_by('-id')
    total_comments = cpost.comments.all().filter(reply=None).order_by('-id')
    tcl = {}
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()
        cliked = False
        if cmt.likes.filter(id=request.user.id).exists():
            cliked = True

        tcl[cmt.id] = cliked

    context = {
        'comment_form': CommentForm(),
        'post': cpost,
        'comments': total_comments,
        'total_clikes': post.total_clikes(),
        'clikes': tcl
    }

    if is_ajax(request=request):
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})


""" Home page with all posts """

from sorl.thumbnail import get_thumbnail

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        from django.core.files.storage import default_storage
        context = super(PostListView, self).get_context_data(**kwargs)
        users = list(User.objects.exclude(pk=self.request.user.pk))
        cnt = min(3, len(users))  # Ensures cnt is not greater than the number of users
        random_users = random.sample(users, cnt)
        context['random_users'] = random_users
        
        # Add thumbnails for each post
        for post in context['posts']:
            if post.image and default_storage.exists(post.image.name):
                post.thumbnail = get_thumbnail(post.image, '100x100', crop='center', quality=99)
            else:
                post.thumbnail = None

        
        return context


""" All the posts of the user """


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


""" Post detail view 


def PostDetailView(request, pk):
    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    total_saves = stuff.total_saves()
    total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
    total_comments2 = stuff.comments.all().order_by('-id')
    post = Post.objects.get(pk=pk)
    media_type = post.get_media_type()

    context = {
        'post': post,
        'media_type': media_type,
    }

    if request.method == "POST":
        comment_qs = None
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            form = request.POST.get('body')
            reply_id = request.POST.get('comment_id')
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            comment = Comment.objects.create(name=request.user, post=stuff, body=form, reply=comment_qs)
            comment.save()
            if reply_id:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form,
                                      notification_type=4)
                notify.save()
            else:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form,
                                      notification_type=3)
                notify.save()
            total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
            total_comments2 = stuff.comments.all().order_by('-id')
    else:
        comment_form = CommentForm()

    tcl = {}
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()
        cliked = False
        if cmt.likes.filter(id=request.user.id).exists():
            cliked = True

        tcl[cmt.id] = cliked
    context["clikes"] = tcl

    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    context["total_likes"] = total_likes
    context["liked"] = liked

    saved = False
    if stuff.saves.filter(id=request.user.id).exists():
        saved = True
    context["total_saves"] = total_saves
    context["saved"] = saved

    context['comment_form'] = comment_form

    context['post'] = stuff
    context['comments'] = total_comments

    if is_ajax(request=request):
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_detail.html', context)
    
    """

def PostDetailView(request, pk):
    model= Post
    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    total_saves = stuff.total_saves()
    total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
    total_comments2 = stuff.comments.all().order_by('-id')
    post = Post.objects.get(pk=pk)

    media_type = stuff.get_media_type()

    # Define variables for video matching
    youtube_match = re.match(r"(https?://)?(www\.)?youtube\.com/watch\?v=([^&]+)", stuff.link)
    instagram_match = re.match(r"(https?://)?(www\.)?instagram\.com/.*/(p|reel)/([^/]+)", stuff.link)
    tiktok_match = re.match(r"(https?://)?(www\.)?tiktok\.com/[^/]+/video/([^?]+)", stuff.link)

    context = {
        'post': stuff,
        'media_type': media_type,
        'youtube_match': youtube_match,
        'instagram_match': instagram_match,
        'tiktok_match': tiktok_match,
    }



    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            form = comment_form.cleaned_data['body']
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            comment = Comment.objects.create(name=request.user, post=stuff, body=form, reply=comment_qs)
            comment.save()
            if reply_id:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form,
                                      notification_type=4)
                notify.save()
            else:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form,
                                      notification_type=3)
                notify.save()
            total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
            total_comments2 = stuff.comments.all().order_by('-id')
    else:
        comment_form = CommentForm()

    tcl = {}
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()
        cliked = cmt.likes.filter(id=request.user.id).exists()  # Optimized check
        tcl[cmt.id] = cliked
    context["clikes"] = tcl

    liked = stuff.likes.filter(id=request.user.id).exists()  # Optimized check
    context["total_likes"] = total_likes
    context["liked"] = liked

    saved = stuff.saves.filter(id=request.user.id).exists()  # Optimized check
    context["total_saves"] = total_saves
    context["saved"] = saved

    context['comment_form'] = comment_form
    context['comments'] = total_comments

    if is_ajax(request=request):
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_detail.html', context)






""" Create post """


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'link', 'vibe', 'caption']

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)

        # Save media to appropriate folder based on type
        media_type = self.object.get_media_type()
        if media_type:
            file_path = f'{media_type}s/{self.object.vibe.name}'
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            fs.save(file_path, self.object.vibe)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'link','vibe', 'caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


""" Search by post title or username """


def search(request):
    query = request.GET['query']
    if len(query) >= 150 or len(query) < 1:
        allposts = Post.objects.none()
    elif len(query.strip()) == 0:
        allposts = Post.objects.none()
    else:
        allpostsTitle = Post.objects.filter(title__icontains=query)
        allpostsAuthor = Post.objects.filter(author__username=query)
        allposts = allpostsAuthor.union(allpostsTitle)

    params = {'allposts': allposts}
    return render(request, 'blog/search_results.html', params)


""" Liked posts """


@login_required
def AllLikeView(request):
    user = request.user
    liked_posts = user.blogpost.all()
    context = {
        'liked_posts': liked_posts
    }
    return render(request, 'blog/liked_posts.html', context)


""" Saved posts """


@login_required
def AllSaveView(request):
    user = request.user
    saved_posts = user.blogsave.all()
    context = {
        'saved_posts': saved_posts
    }
    return render(request, 'blog/saved_posts.html', context)


