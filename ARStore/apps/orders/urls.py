from django.urls import path

from ARStore.apps.orders.views import add

app_name = 'orders'
urlpatterns = [
    path('add/', add, name='add')
]
