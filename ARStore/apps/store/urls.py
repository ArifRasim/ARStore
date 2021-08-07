from django.urls import path

from ARStore.apps.store import views
from ARStore.apps.store.views import IndexView, ProductDetailView, CategoryView

app_name = 'store'

urlpatterns = [
    path('', IndexView.as_view(),name='all_products' ),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>', CategoryView.as_view(), name='category_list'),
    path('search/', views.search_products, name='search_products'),
]
