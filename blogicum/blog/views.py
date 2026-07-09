from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from .models import Post, Category, User, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, PostForm, CustomUserCreationForm

from django.db.models import Count
from django.utils import timezone
from django.shortcuts import redirect


class PostDeleteView(LoginRequiredMixin, DeleteView):
    post_obj = None
    model = Post
    template_name = 'blog/detail.html'  # свой шаблон для формы поста, не comment.html
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        return context

class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'  # свой шаблон для формы поста, не comment.html
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    post_obj = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=self.post_obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_obj.pk})
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if comment.author != request.user:
            raise PermissionDenied("Вы можете удалять только свои комментарии")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_obj.pk})
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свой профиль")
        return obj

    def get_success_url(self):
        # self.object уже содержит актуальные (сохранённые) данные после form_valid
        return reverse('blog:profile', kwargs={'username': self.object.username})
    
class UserDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.posts.select_related(
            'author', 'location', 'category'
        )

        # если смотрит не сам автор — скрываем неопубликованное
        if self.request.user != self.object:
            posts = posts.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )

        posts = posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context
    
class PostsListView(ListView):
    model = Post
    ordering = '-pub_date'  # обычно посты сортируют по дате публикации, а не id
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'location', 'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'pk' 

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.author == self.request.user:
            # автор видит свой пост в любом случае
            return post
        # для всех остальных — только опубликованные посты
        post = get_object_or_404(
            Post,
            pk=self.kwargs['pk'],
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context

class CategoryPostsListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_category(self):
        # Кэшируем, чтобы не делать запрос дважды (в get_queryset и get_context_data)
        if not hasattr(self, '_category'):
            self._category = get_object_or_404(
                Category.objects.filter(is_published=True),
                slug=self.kwargs['category_slug'],
            )
        return self._category

    def get_queryset(self):
        category = self.get_category()
        return Post.objects.select_related(
            'category', 'author', 'location'
        ).filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now(),
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context