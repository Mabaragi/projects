from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout

# Create your views here.


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
    


def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('movies:index')
    else:
        form = CustomUserChangeForm()
    context = { 'form': form }
    return render(request, 'accounts/update.html', context)

def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

def change_password(request):
    user = request.user
    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(user)
    context = {'form': form }
    return render(request, 'accounts/change_password.html', context)

def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username = username)
    context ={'person':person}
    return render(request, 'accounts/profile.html', context)

def follow(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    User = get_user_model()
    person = User.objects.get(pk=pk)
    if request.user == person:
        return redirect('accounts:profile', person.username)
    if person.followings.filter(pk=request.user.pk).exists():
        person.followings.remove(request.user)
    else:
        person.followings.add(request.user)
    return redirect('accounts:profile', person.username)