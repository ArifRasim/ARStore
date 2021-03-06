from django.urls import path

from ARStore.apps.cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_summary'),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('update/', views.cart_update, name='cart_update'),
]