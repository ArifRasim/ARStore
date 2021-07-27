from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import path
from django.views.generic import TemplateView

from accounts.forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm
from accounts.views import register_view, activate_account, dashboard, edit_details, delete_user, addresses_view, \
    add_address, edit_address, delete_address, set_default_address

app_name = 'account'
urlpatterns = [
    path('register/', register_view, name='register_view'),
    path('activate/<slug:uidb64>/<slug:token>', activate_account, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/user/password_reset_form.html',
                                                      success_url='password_reset_email_confirm',
                                                      email_template_name='accounts/user/password_reset_email.html',
                                                      form_class=PwdResetForm), name='password_reset_form'),
    path('password_reset_confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='accounts/user/password_reset_confirm.html',
                                          success_url='password_reset_complete',
                                          form_class=PwdResetConfirmForm), name='password_reset_confirm'),
    path('password_reset/password_reset_email_confirm',
         TemplateView.as_view(template_name='accounts/user/reset_status.html'),
         name='password_reset_status'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login/login.html', form_class=UserLoginForm, )
         , name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('profile/edit/', edit_details, name='edit_view'),
    path('profile/delete/', delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name='accounts/user/delete_confirm.html'),
         name='delete_confirm'),
    path('adresses/', addresses_view, name='addresses'),
    path('adresses/add/', add_address, name='add_address'),
    path('adresses/edit/<slug:id>', edit_address, name='edit_address'),
    path('adresses/delete/<slug:id>', delete_address, name='delete_address'),
    path('adresses/default/<slug:id>', set_default_address, name='set_default_address'),

]
