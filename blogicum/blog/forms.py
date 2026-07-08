from django import forms
from .models import Comment, Post
from django.core.exceptions import ValidationError

from django.core.mail import send_mail

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',) 

class PostForm(forms.ModelForm):
    # first_name = forms.CharField(label='Имя', max_length=20)
    # last_name = forms.CharField(
    #     label='Фамилия', required=False, help_text='Необязательное поле'
    # )
    # birthday = forms.DateField(
    #     label='Дата рождения',
    #     # Указываем, что виджет для ввода даты должен быть с типом date.
    #     widget=forms.DateInput(attrs={'type': 'date'})
    # ) 
    text = forms.Textarea()
    pub_date = forms.DateTimeField(
        label='Дата и время публикации',
        # Указываем, что виджет для ввода даты должен быть с типом date.
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    ) 

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', 'created_at')
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }