from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, Post
from django.contrib.auth.models import User, Group, Permission


class RegisterForm(forms.ModelForm):
    grupo = forms.MultipleChoiceField(
        choices=((choice.id, choice.name) for choice in Group.objects.all()),
        label="Grupos",
        required=False
    )
    permisos = forms.MultipleChoiceField(
        choices=((choice.id, choice.name)
                 for choice in Permission.objects.all()),
        label="Permisos",
        required=False
    )
    password2 = forms.PasswordInput()

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if(password != password2):
            raise ValidationError('Las contraseñas no coinciden.')
        return password2

    class Meta:
        model = User
        fields = ("username", "email", "password")




class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput,
        required=True,
        min_length=6,
        )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
        required=True,
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug','body')
