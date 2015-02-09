from django.contrib.auth.decorators import user_passes_test
from .models import *

def logged_in_user_has_profile(user):
    """
    Function that checks if a logged in user has profile
    """
    if user.is_anonymous():
        return True
    else:
        return UserProfile.objects.filter(user=user).exists()


def check_if_user_has_profile(function=None):
    """
    Decorator for views that checks that if the user is logged 
    in it has also an UserProfile. If not, it redirects to 'create_profile'
    """
    actual_decorator = user_passes_test(
        lambda u: logged_in_user_has_profile(u),
        login_url='create_profile'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator