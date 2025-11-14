from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """
    Decorator to ensure only staff/admin users can access a view.
    Redirects non-staff to user dashboard with error message.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    """
    Decorator to ensure only non-admin users can access a view.
    Redirects staff to admin dashboard.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(allowed_roles):
    """
    Decorator to check if user has specific role from CustomUser.role field.
    Usage: @role_required(['admin', 'teacher'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_role = getattr(request.user, 'role', 'student')
            if user_role not in allowed_roles:
                messages.error(request, f'Access denied. Required role: {", ".join(allowed_roles)}')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
