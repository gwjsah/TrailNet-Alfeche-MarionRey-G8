from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .decorators import role_required
from .forms import RiderRegistrationForm

User = get_user_model()


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
    """Route logged-in users to the dashboard matching their role."""
    if request.user.is_trail_admin():
        return redirect('accounts:admin_dashboard')
    return redirect('accounts:rider_dashboard')


@role_required(User.ROLE_RIDER)
def rider_dashboard_view(request):
    """Dashboard for Riders showing trail activity, ride events, and bike setup."""
    return render(request, 'accounts/rider_dashboard.html')


@role_required(User.ROLE_ADMIN)
def admin_dashboard_view(request):
    """Dashboard for Trail Admins showing trail management and moderation overview."""
    total_riders = User.objects.filter(role=User.ROLE_RIDER).count()
    total_admins = User.objects.filter(role=User.ROLE_ADMIN).count()
    return render(
        request,
        'accounts/admin_dashboard.html',
        {
            'total_riders': total_riders,
            'total_admins': total_admins,
        },
    )
