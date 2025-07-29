from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.contrib import messages

def authenticated_user(view_fun):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect('customers.customer_profile')
        return view_fun(request)
    return wrapper

def admin_only(view_fun):
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect('login')

        group = request.user.groups.first()
        if group is None and request.user.is_superuser:
            return view_fun(request)
            
        if group and group.name == 'admin':
            return view_fun(request)

        if group and group.name == 'customer':
            return redirect('customers.customer_profile')
        
        return redirect('login')
    return wrapper

def allowed_roles(roles=[]):
    def decorator(view_fun):
        def wrapper(request, *args, **kwargs):
            # Staff and superusers always get access
            if request.user.is_staff or request.user.is_superuser:
                # Add staff context to the view
                def wrapped_view(request, *args, **kwargs):
                    response = view_fun(request, *args, **kwargs)
                    if hasattr(response, 'context_data'):
                        response.context_data['is_staff_view'] = True
                    return response
                return wrapped_view(request, *args, **kwargs)
            
            # Check group permissions for regular users
            group = request.user.groups.first()
            if group and group.name in roles:
                return view_fun(request, *args, **kwargs)
            else:
                messages.error(request, 'У вас нет прав для доступа к этой странице')
                return redirect('customers.customer_profile')
        return wrapper
    return decorator