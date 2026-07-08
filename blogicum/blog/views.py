from django.shortcuts import render, get_list_or_404, get_object_or_404
# from django.http import HttpResponse
# from django.utils import timezone
from datetime import datetime

from .models import Post, Category


# Create your views here.
def index(request):
    """дата публикации — не позже текущего времени,
        значение поля is_published равно True,
        у категории, к которой принадлежит публикация, значение поля is_published равно True."""
    template = 'blog/index.html'
    posts = Post.objects.select_related('category','author','location').filter(
        pub_date__lt=datetime.now(),
        is_published=True,
        category__is_published=True   
    )[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category','author','location').filter(
        pub_date__lt=datetime.now(),
        is_published=True,
        category__is_published=True,
        pk=id
        )
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    posts = get_list_or_404(
        Post.objects.select_related('category','author','location').filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lt=datetime.now()
        )   
    )
    category = get_object_or_404(
        Category.objects.values('title', 'description').filter(
            slug=category_slug,
            is_published=True
        )[:1]
    )
    context = {
        'post_list': posts,
        'category': category,
    }
    return render(request, template, context)
