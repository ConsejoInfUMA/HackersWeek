from django.contrib.auth.decorators import user_passes_test

def check_is_staff(function=None):
    """
    Decorator for views that checks if the user is staff
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url='home',
    )
    if function:
        return actual_decorator(function)
    return actual_decorator