from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'লগইন সফল!')
                next_url = request.GET.get('next', 'accounts:dashboard')  # নেমস্পেস যোগ করুন
                return redirect(next_url)
            else:
                messages.error(request, 'ভুল ইউজারনেম বা পাসওয়ার্ড।')
        else:
            messages.error(request, 'ফর্মে ত্রুটি রয়েছে।')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'অ্যাকাউন্ট তৈরি সফল! লগইন করুন।')
            return redirect('accounts:login')  # নেমস্পেস যোগ করুন
        else:
            messages.error(request, 'ফর্মে ত্রুটি রয়েছে।')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'লগআউট সফল!')
    return redirect('core:home')  # নেমস্পেস ইতিমধ্যে সঠিক