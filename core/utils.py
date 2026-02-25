import re
from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    """
    Decorator for views that checks that the user is a superuser,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/',  # Redirect URL for non-superusers
    )
    return actual_decorator(view_func)

def is_valid_email(email):
    
    # Regular expression for a valid email
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))