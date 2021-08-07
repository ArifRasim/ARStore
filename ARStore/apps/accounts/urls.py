from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from ARStore.apps.accounts.forms import UserLoginForm
from ARStore.apps.accounts.views import edit_details, delete_user, addresses_view, \
    add_address, edit_address, delete_address, set_default_address, add_to_wishlist, wishlist, user_orders, \
    DashboardView, register_view

app_name = 'account'
urlpatterns = [
    path('register/', register_view, name='register_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login/login.html', form_class=UserLoginForm, )
         , name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('edit/', edit_details, name='edit_view'),
    path('delete/', delete_user, name='delete_user'),
    path('delete_confirm/', TemplateView.as_view(template_name='accounts/user/delete_confirm.html'),
         name='delete_confirm'),
    path('adresses/', addresses_view, name='addresses'),
    path('add_address/', add_address, name='add_address'),
    path('adresses/edit/<slug:id>', edit_address, name='edit_address'),
    path('adresses/delete/<slug:id>', delete_address, name='delete_address'),
    path('adresses/default/<slug:id>', set_default_address, name='set_default_address'),
    path('wishlist/add/<int:id>', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('orders/', user_orders, name='user_orders'),

]
