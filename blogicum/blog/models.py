from django.db import models
from core.models import PublishedModel, DatetimeModel
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(PublishedModel, DatetimeModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    location = models.ForeignKey(
        'Location',
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Локация'
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'Посты' 

    def __str__(self):
        return self.title 


class Category(PublishedModel, DatetimeModel):
    title = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории' 

    def __str__(self):
        return self.title 
    

class Location(PublishedModel, DatetimeModel):
    name = models.CharField(max_length=256, verbose_name='Локация')

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'Локации' 

    def __str__(self):
        return self.title 
    
