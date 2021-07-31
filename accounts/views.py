from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode

from accounts.forms import RegisterForm, UserEditForm, UserAddressForm
from accounts.models import Customer, Address
from accounts.token import account_activation_token
from orders.models import Order
from orders.views import user_orders
from store.models import Product


def dashboard(request):
    orders = user_orders(request)
    return render(request, 'accounts/user/dashboard.html', {'orders': orders})
    # {'section': 'profile',
    #  'orders': orders})


def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['user_name']
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('accounts/register/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }
                                       )
            user.email_user(subject=subject, message=message)
            user.is_active = True
            return render(request, 'accounts/register/account_activation_email.html',
                          {'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                           'token': account_activation_token.make_token(user)})
        else:
            return redirect('account:login')
    else:
        form = RegisterForm()
        return render(request, 'accounts/register/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_encode(uidb64))
        user = Customer.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('store:all_products')
    except:
        pass


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'accounts/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('store:all_products')


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
        address_form = UserAddressForm(instance=address)
    return render(request, 'accounts/user/add_address.html', {"form": address_form})


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


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, 'Removed ' + product.title + ' from your wishlist')

    else:
        product.user_wishlist.add(request.user)
        messages.success(request, 'Added ' + product.title + ' to your wishlist')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    return render(request, 'accounts/user/wishlist.html', {'wishlist': products})

@login_required
def user_orders(request):
    user_id=request.user.id
    orders=Order.objects.filter(user_id=user_id)

    return render(request,'accounts/user/user_orders.html',{'orders':orders})