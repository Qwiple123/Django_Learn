from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from .models import Post, LikedPost
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.http import HttpResponseRedirect




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.name = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.edit_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def view_profile(request):
    posts = Post.objects.filter(author = request.user)
    return render(request, 'blog/profile.html', {'posts': posts})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    liked_post, created = LikedPost.objects.get_or_create(
        post = post,
        user = request.user
    )
    if not created:
        liked_post.delete()
    else:
        liked_post.save()

    return redirect('post_list')