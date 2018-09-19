from django.contrib import messages
from django.contrib.auth import (authenticate, login as django_login,
                                 logout as django_logout)
from django.shortcuts import render, redirect
from account.models import User
from fudbyte.utils.models import get_object_or_none
from .forms import RegistrationForm, RecoverPasswordForm


def register(request):
    form = RegistrationForm()
    if request.method == "POST":
        next_page = request.GET.get('next', None)
        form = RegistrationForm(request.POST)
        error_return_url = '/register{}'.format('&next='+next_page if next_page else '')
        if form.is_valid():
            fdata = form.cleaned_data
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.add_message(request, messages.ERROR, message='This Email Address is already in use')
                return redirect(error_return_url)
            User.create_user(fdata['first_name'], fdata['last_name'], fdata['email'], fdata['password'], fdata['gender'])
            messages.add_message(request, messages.SUCCESS, message='Account Registration Successful.')
            if next_page:
                return redirect(next_page)
            return redirect('/accounts/login')
    return render(request, 'account/register.html', {'form': form,
                                                     'page_title': 'Sign Up'})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_page = request.GET.get('next')
        user = authenticate(username=email, password=password)
        if user is not None:
            django_login(request, user)
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, message='Wrong email or password')
            return redirect('/accounts/login')
    return render(request, 'account/login.html', {'page_title': 'Sign In'})

#
# def recover_password_request(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = get_object_or_none(User, email=email)
#         if user:
#             send_forget_password_link.delay(user.id)
#             messages.add_message(request, messages.SUCCESS, message='Email Sent on how to recover your password')
#             return redirect('/')
#         else:
#             messages.add_message(request, messages.ERROR, message='Wrong email entered')
#         return redirect('/')


def process_reset_password(request, *args, **kwargs):
    code = kwargs.get('url_token', None)
    user = get_object_or_none(User, forget_password_link=code, forget_password_status=False)
    form = RecoverPasswordForm()
    if not user:
        messages.add_message(request, messages.ERROR, message='Wrong recover password url')
    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, message='New Password Set')
            return redirect('/')
    return render(request, 'accounts/recover.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect('/')