from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from ARStore.apps.accounts.models import Customer, Address


class RegisterForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(
        label='Enter Your Email', min_length=4, max_length=110,
        error_messages={'required': 'Sorry you will need an email'}
    )
    password = forms.CharField(label='Enter your Password', widget=forms.PasswordInput, help_text='Required')

    repeat_password = forms.CharField(label='Repeat your Password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        user = Customer.objects.filter(name=user_name)
        if user.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_repeat_password(self):
        password = self.cleaned_data['password'].lower()
        repeat_password = self.cleaned_data['repeat_password'].lower()
        if password != repeat_password:
            raise forms.ValidationError('Passwords do not match !')
        return password

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = Customer.objects.filter(email=email)
        if user.count():
            raise forms.ValidationError('Email is already taken !')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['repeat_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control ', 'placeholder': 'Password', 'id': 'login-password'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Full Name', 'id': 'form-lastname'}))

    class Meta:
        model = Customer
        fields = ('email', 'name',)


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunately we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line_1", "address_line_2", "city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name",}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line_1"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["address_line_1"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address"})
        self.fields["address_line_2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address"}
        )
        self.fields["city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "City"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Post Code"}
        )
        self.fields["address_line_1"].label = 'Address 1'
        self.fields["address_line_2"].label = 'Address 2'

