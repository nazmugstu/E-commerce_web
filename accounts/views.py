from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ProfileUpdateForm


from .forms import LoginForm, RegisterForm, ProfileUpdateForm

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



@login_required
def profile_update(request):
    if request.method == 'POST':
        print(request.POST)  # ফর্ম ডাটা ডিবাগ করার জন্য
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            # User মডেলের তথ্য আপডেট
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            # Profile মডেলের তথ্য আপডেট
            form.save()
            return redirect('accounts:dashboard')
        else:
            print(form.errors)  # ফর্ম ত্রুটি ডিবাগ করার জন্য
    else:
        form = ProfileUpdateForm(
            instance=request.user.profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )
    return render(request, 'accounts/profile_update.html', {'form': form})