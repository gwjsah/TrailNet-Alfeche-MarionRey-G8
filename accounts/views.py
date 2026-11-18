from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RiderRegistrationForm


def register_view(request):
    """Handle new user registration with validation and hashed password storage."""
    if request.user.is_authenticated:
        return redirect('accounts:register')

    if request.method == 'POST':
        form = RiderRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Account created successfully! You can now log in with your credentials.',
            )
            return redirect('accounts:register')
        messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = RiderRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
