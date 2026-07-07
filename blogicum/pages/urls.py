# Адрес	                            Приложение	Функция-обработчик	Имя шаблона
# pages/about/	                    pages	    about	            about.html
# pages/rules/	                    pages	    rules	            rules.html

from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('rules/', views.rules, name='rules'),
]
