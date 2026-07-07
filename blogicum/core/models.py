from django.db import models


class PublishedModel(models.Model):
    """Абстрактная модель. Добвляет флаг is_published."""
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        abstract = True

class DatetimeModel(models.Model):
    """Абстрактная модель. Добавляет дату создания"""
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Добавлено',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True