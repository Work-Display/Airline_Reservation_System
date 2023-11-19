from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from .dal import get_role_by_user
import logging 
logger = logging.getLogger("pick.me") 


def anonymous_only(view_func):
    """
    Example usage: redirecting a logged user to their profile page whenever they try to access the login page manually.
    """

    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_roles(allowed_roles=[]):
    """
    Helps with setting permissions according to the current user's role.
    If the user's role name is in allowed_roles a permission is granted. 
    Otherwise it gets denied and an HttpResponse with a warning message gets returned.
    * Because 'Anonymous' isn't an actual user role name since it refers to non-users,
    if allowed_roles==['Anonymous'], it checks if a user is logged in to know whether or not to grant a permission.
    """
    def decorator(view_func):

        def wrapper_func(request, *args, **kwargs):

            if ((type(allowed_roles) != list)):
                err_msg = f"Bad input. 'allowed_roles' must be a list of strings for this decorator to work. Error: {e}"
                logger.error(err_msg)
                return HttpResponse(warning_msg)
            
            if not(all(map(lambda x: isinstance(x, str), allowed_roles))):
                err_msg = f"Bad input. 'allowed_roles' must be a list of strings for this decorator to work. Error: {e}"
                logger.error(err_msg)
                return HttpResponse(warning_msg)
            
            if (allowed_roles==['Anonymous']):
                logged = bool('user_token' in request.session)
                if logged:
                    warning_msg = f"Logged in users are not authorized to view this page. To view it you should first log out."
                    return HttpResponse(warning_msg)
                else:
                    return view_func(request, *args, **kwargs)

            warning_msg = f"You are not authorized to view this page. Only users with the following roles: {allowed_roles} can access this page."

            try:
                user_id = 0   
                user_token = 0         
                user_token = request.session['user_token']
                user_id = Token.objects.get(key=user_token).user.id
            except Exception as e:
                err_msg = f"Failed to get authentication token. Error: {e} {user_token = }. {user_id = }"
                logger.error(err_msg)
                return HttpResponse(warning_msg)

            role_name = get_role_by_user(user_id=user_id) 
            if role_name==False:
                err_msg = f"Failed to get a user's ({user_id = }) role name. Error: {e}"
                logger.error(err_msg)
                return HttpResponse(warning_msg)
            
            if role_name in allowed_roles:
                print(f"It's working! {role_name = }, {allowed_roles = }.")
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(warning_msg)
                
            
        return wrapper_func
    return decorator

