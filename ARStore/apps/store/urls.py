from django.urls import path

from ARStore.apps.store import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products,name='all_products' ),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('category/<slug:slug>', views.category_list, name='category_list'),
]
