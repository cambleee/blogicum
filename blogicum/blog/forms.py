from django import forms
from .models import Comment, Post
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
    pub_date = forms.DateTimeField(
        label='Дата и время публикации',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    ) 

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', 'created_at')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
