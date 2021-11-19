from django.contrib.auth import get_user_model, authenticate, login as login_user, logout as logout_user
from django.shortcuts import render, redirect
from django.urls import reverse

from authentication.forms import RegistrationForm, LoginForm

User = get_user_model()


def reg(request):
    if request.user.is_authenticated:
        return redirect(reverse('catalog:home'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            return redirect(reverse('catalog:home'))
    else:
        form = RegistrationForm()

    return render(request,
                  'authentication/reg.html',
                  {'form': form}

                  )


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('catalog:home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                email=form.cleaned_data['email_or_username'],
                                username=form.cleaned_data['email_or_username'],
                                password=form.cleaned_data['password']
                                )
            if user:
                redirect_url = request.GET.get('next') or reverse('catalog:home')
                login_user(request, user)
                return redirect(redirect_url)
    else:
        form = LoginForm()
    next_url = request.GET.get('next', '')
    return render(
        request,
        'authentication/login.html',
        {'form': form, 'next': next_url}
    )


def logout(request):
    logout_user(request)
    return redirect(reverse('catalog:home'))

def account(request):
    user = request.user
    return render(
        request,
        'authentication/account.html',
        {'user': user}
    )

