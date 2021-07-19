from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode

from accounts.forms import RegisterForm, UserEditForm
from accounts.models import UserBase
from accounts.token import account_activation_token
from orders.views import user_orders


def dashboard(request):
    orders = user_orders(request)
    return render(request, 'accounts/user/dashboard.html',{'orders':orders})
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
            user.set_password = form.cleaned_data['password']
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('accounts/register/account_activation_email.html'), {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }
            user.email_user(subject=subject, message=message)
        return HttpResponse('activation sent ')
    else:
        form = RegisterForm()
        return render(request, 'accounts/register/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_encode(uidb64))
        user = UserBase.objects.get(pk=uid)
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
    user = UserBase.objects.get(username=request.user)
    user.is_active=False
    user.save()
    logout(request)
    return redirect('store:all_products')
