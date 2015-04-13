# -*- coding: utf-8 -*-

from main.models import UserProfile, RoleRequest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя *'
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
        self.fields['password1'].label = 'Пароль *'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        self.fields['password2'].label = 'Подтверждения пароля *'
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Пользователь с таким email адресом уже зарегистрирован')
        return email
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        
    email = forms.EmailField(required=True, label='Email *', widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class UserProfileRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = 'ФИО *'
        self.fields['full_name'].widget = forms.TextInput(attrs={'placeholder': 'Иван Иванович Иванов'})
        
    class Meta:
        model = UserProfile
        exclude = ('user', 'role', 'activation_key')


class UserRoleRequestForm(forms.ModelForm):
    class Meta:
        model = RoleRequest
        exclude = ('user',)