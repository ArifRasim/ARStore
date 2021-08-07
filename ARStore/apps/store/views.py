import products as products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
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


# class SearchView(ListView):
#     model = Product
#     template_name = 'store/search_products.html'
#     context_object_name = 'products'
#     paginate_by = 3
#
#     def get_queryset(self):
#         qs = super(SearchView, self).get_queryset()
#         q = self.kwargs.get('q')
#         if not q:
#             q=''
#         products = Product.objects.all()
#         # if q:
#         #     products = Product.objects.filter(title__contains=q)
#
#         return qs.filter()


# def all_products(request):
#     products = Product.objects.all()
#     pagination = Paginator(products, 6)
#     page = request.GET.get('page')
#     product_list = pagination.get_page(page)
#     return render(request, 'store/index.html', {'products': product_list})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/products/product.html'
    slug_field = 'slug'  # slug field
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['product'] = get_object_or_404(Product, slug=kwargs['slug'])
    #     return context


# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     user = request.user
#     context = {
#         'product': product,
#         'user': user
#     }
#     return render(request, 'store/products/product.html', context)


# def category_list(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     products = Product.objects.filter(category=category)
#     pagination = Paginator(products, 3)
#     page = request.GET.get('page')
#     product_list = pagination.get_page(page)
#     context = {
#         'category': category,
#         'products': product_list
#     }
#     return render(request, 'store/categories/category.html', context)


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
