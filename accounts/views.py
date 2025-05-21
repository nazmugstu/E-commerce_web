from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ProfileUpdateForm
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                next_url = request.GET.get('next', 'accounts:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Form contains errors.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure Profile is created (in case signal fails)
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Form contains errors.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('core:home')

@login_required
def profile_update(request):
    # Check if Profile exists, create one if it doesn't
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        messages.info(request, 'Profile created for your account.')

    if request.method == 'POST':
        print(request.POST)  # Debug form data
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Update CustomUser fields
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            # Update Profile fields
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:dashboard')
        else:
            print(form.errors)  # Debug form errors
            messages.error(request, 'Form contains errors.')
    else:
        form = ProfileUpdateForm(
            instance=profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )
    return render(request, 'accounts/profile_update.html', {'form': form})