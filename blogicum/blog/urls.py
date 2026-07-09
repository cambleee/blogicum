# Адрес	                            Приложение	Функция-обработчик	Имя шаблона
# ''	                            blog	    index	            index.html
# posts/<int:id>/	                blog	    post_detail	        detail.html
# category/<slug:category_slug>/	blog	    category_posts	    category.html


from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.index, name='index'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('', views.PostsListView.as_view(), name='index'),
    # path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('profile/<slug:username>/edit/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('profile/<slug:username>/', views.UserDetailView.as_view(), name='profile'),
    path('category/<slug:category_slug>/', views.CategoryPostsListView.as_view(), name='category_posts'),
    path('posts/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    # path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
        
]
