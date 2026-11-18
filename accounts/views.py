from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RiderRegistrationForm


def register_view(request):
    """Handle new user registration with validation and hashed password storage."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = RiderRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Account created successfully! You can now log in with your credentials.',
            )
            return redirect('accounts:login')
        messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = RiderRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Authenticate a user and start a session, showing clear errors on failure."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            return redirect('accounts:dashboard_redirect')
        messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        'accounts/login.html',
        {'form': form, 'next': request.GET.get('next', '')},
    )


@require_POST
@login_required
def logout_view(request):
    """End the current user session and redirect to the login page."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def dashboard_redirect_view(request):
    """Protected landing view for logged-in users (role routing added next)."""
    return render(request, 'accounts/dashboard_placeholder.html')
