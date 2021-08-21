from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from ARStore.apps.accounts.forms import RegisterForm, UserEditForm, UserAddressForm
from ARStore.apps.accounts.models import Customer, Address
from ARStore.apps.orders.models import Order
from ARStore.apps.store.models import Product


class DashboardView(LoginRequiredMixin, TemplateView):
    model = Customer
    template_name = 'accounts/user/dashboard.html'


class RegisterView(CreateView):
    model = Customer
    fields = ['email', 'name', 'password']
    template_name = 'accounts/register/register.html'


@login_required
def delete_user(request):
    user = Customer.objects.get(id=request.user.id)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirm')


@login_required
def delete_address(request, id):
    Address.objects.get(pk=id, customer=request.user).delete()
    return HttpResponseRedirect(reverse('account:addresses'))


@login_required
def set_default_address(request, id):
    Address.objects.filter(default=True, customer=request.user).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    if 'delivery_address' in request.META.get('HTTP_REFERER'):
        return redirect('checkout:delivery_address')
    else:
        return HttpResponseRedirect(reverse('account:addresses'))


def register_view(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['user_name']
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            return render(request, 'accounts/register/account_activation_email.html', )

        else:
            messages.success(request, 'There was an error try again')
            return render(request, 'accounts/register/register.html', status=400)
    else:
        form = RegisterForm()
        return render(request, 'accounts/register/register.html', {'form': form})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your changes were applied successfully.')
        else:
            messages.success(request, 'There was an error try again')
            return render(request, 'accounts/user/edit_details.html', status=400)
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'accounts/user/edit_details.html', {'user_form': user_form})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, 'Removed ' + product.title + ' from your wishlist')

    else:
        product.user_wishlist.add(request.user)
        messages.success(request, 'Added ' + product.title + ' to your wishlist')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def addresses_view(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, 'accounts/user/addresses.html', {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
        else:
            messages.success(request, 'There was an error try again')
            return render(request, 'accounts/user/add_address.html', status=400)
    else:
        address_form = UserAddressForm()
    return render(request, 'accounts/user/add_address.html', {"form": address_form})


@login_required
def edit_address(request, id):
    address = Address.objects.get(pk=id, customer=request.user)
    if request.method == 'POST':
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
        else:
            return HttpResponse('Bad request!', status=400)
    else:
        address_form = UserAddressForm(instance=address)
    return render(request, 'accounts/user/add_address.html', {"form": address_form})


@login_required
def wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    pagination = Paginator(products, 2)
    page = request.GET.get('page')
    products = pagination.get_page(page)
    return render(request, 'accounts/user/wishlist.html', {'wishlist': products})


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)

    pagination = Paginator(orders, 2)
    page = request.GET.get('page')
    orders = pagination.get_page(page)
    return render(request, 'accounts/user/user_orders.html', {'orders': orders})
