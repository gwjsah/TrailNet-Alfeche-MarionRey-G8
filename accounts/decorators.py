from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def role_required(*allowed_roles):
    """Restrict a view to logged-in users whose role is in allowed_roles."""
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.user.role
            if request.user.is_superuser and 'admin' in allowed_roles:
                return view_func(request, *args, **kwargs)
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return render(
                request,
                'accounts/access_denied.html',
                status=403,
            )

        return _wrapped_view

    return decorator
