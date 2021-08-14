from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from ARStore.apps.store.models import Product, Category


class IndexView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'
    paginate_by = 6


class CategoryView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return qs.filter(category=category)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/products/product.html'
    slug_field = 'slug'  # slug field






def search_products(request):
    q = request.POST.get('q')
    products = Product.objects.all()
    if q:
        products = Product.objects.filter(title__contains=q)

    paginator = Paginator(products, 9)
    page = request.POST.get('page', 1)
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
    return render(request, 'store/search_products.html', {'products': product_list})
