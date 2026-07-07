"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Адрес	                            Приложение	Функция-обработчик	Имя шаблона
# ''	                            blog	    index	            index.html
# posts/<int:id>/	                blog	    post_detail	        detail.html
# category/<slug:category_slug>/	blog	    category_posts	    category.html
# pages/about/	                    pages	    about	            about.html
# pages/rules/	                    pages	    rules	            rules.html

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    
    # path('posts/', include('blog.urls', namespace='blog')),
    # path('category/', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
]
