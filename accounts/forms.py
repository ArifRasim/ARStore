from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from accounts.models import UserBase


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Your Username', min_length=4, max_length=50,
    )
    # first_name = forms.CharField(
    #     label='Enter Your First Name', min_length=4, max_length=50, help_text='Required'
    # )
    # last_name = forms.CharField(
    #     label='Enter Your Last Name', min_length=4, max_length=50, help_text='Required'
    # )
    email = forms.EmailField(
        label='Enter Your Email', min_length=4, max_length=110,
        error_messages={'required': 'Sorry you will need an email'}
    )
    password = forms.CharField(label='Enter your Password', widget=forms.PasswordInput, help_text='Required')

    repeat_password = forms.CharField(label='Repeat your Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        user = UserBase.objects.filter(username=username)
        if user.count():
            raise forms.ValidationError('Username is already taken !')
        return username

    def clean_repeat_password(self):
        password = self.cleaned_data['password'].lower()
        repeat_password = self.cleaned_data['repeat_password'].lower()
        if password != repeat_password:
            raise forms.ValidationError('Passwords do not match !')
        return password

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = UserBase.objects.filter(email=email)
        if user.count():
            raise forms.ValidationError('Email is already taken !')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['repeat_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control ', 'placeholder': 'Password', 'id': 'login-password'}))

class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

