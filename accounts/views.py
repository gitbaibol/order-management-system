from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import authenticated_user, admin_only, allowed_roles
from accounts.models import *
from accounts.forms import *
from .filters import *

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    # For non-staff users, show their profile
    if not request.user.is_staff:
        return redirect('customers.customer_profile')

    # For staff, show the admin dashboard
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')
    total = orders.count()
    delivered = Order.objects.filter(status="Готов").count()
    in_progress = Order.objects.filter(status="В работе").count()
    pending = Order.objects.filter(status="В ожидании").count()

    context = {
        'customers': customers,
        'orders': orders[:10],  # Last 10 orders
        'total': total,
        'delivered': delivered,
        'in_progress': in_progress,
        'pending': pending,
        'total_customers': customers.count()
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def customer_profile(request):
    print('User:', request.user)
    print('Groups:', list(request.user.groups.all()))
    print('Authenticated:', request.user.is_authenticated)
    
    # If user is staff, redirect to dashboard
    if request.user.is_staff:
        return redirect('dashboard')
        
    try:
        customer = request.user.customer
        orders = customer.order_set.all().order_by('-date_created')
        
        total_orders = orders.count()
        delivered = orders.filter(status='Готов').count()
        pending = orders.filter(status='В ожидании').count()
        in_progress = orders.filter(status='В работе').count()
        
        # Get the last 5 orders after counting
        recent_orders = orders[:5]

        context = {
            'orders': recent_orders,
            'total_orders': total_orders,
            'delivered': delivered,
            'pending': pending,
            'in_progress': in_progress,
            'customer': customer
        }
    except Exception as e:
        print('Error:', str(e))
        context = {
            'orders': [],
            'total_orders': 0,
            'delivered': 0,
            'pending': 0,
            'in_progress': 0
        }
    return render(request, 'accounts/customer_profile.html', context)


@login_required(login_url='login')
def customer_profile_setting(request):
    if not hasattr(request.user, 'customer'):
        Customer.objects.create(user=request.user)
    
    form = CustomerProfile(instance=request.user.customer)
    if request.method == "POST":
        form = CustomerProfile(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('customers.customer_profile')
    return render(request, 'accounts/profile_setting.html', {
        'form': form
    })

@login_required(login_url='login')
def customers(request, id):
    try:
        customer = Customer.objects.get(id=id)
        
        # Regular users can only view their own profile
        if not request.user.is_staff and request.user.customer != customer:
            messages.error(request, 'У вас нет доступа к этому профилю')
            return redirect('customers.customer_profile')
        
        orders = customer.order_set.all().order_by('-date_created')
        order_count = orders.count()
        
        # Get status counts
        total_orders = orders.count()
        delivered = orders.filter(status='Готов').count()
        in_progress = orders.filter(status='В работе').count()
        pending = orders.filter(status='В ожидании').count()
        
        filterObj = OrderFilter(request.GET, queryset=orders)
        orders = filterObj.qs
        
        context = {
            'customer': customer,
            'orders': orders,
            'order_count': order_count,
            'filterObj': filterObj,
            'total_orders': total_orders,
            'delivered': delivered,
            'in_progress': in_progress,
            'pending': pending
        }
        return render(request, 'accounts/customers.html', context)
    except Customer.DoesNotExist:
        messages.error(request, 'Клиент не найден')
        return redirect('dashboard')

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def products(request):
    # return HttpResponse('contact pafe')
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products' : products
    })



@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def orderCreate(request, customerId):
    try:
        customer = Customer.objects.get(id=customerId)
        OrderFormSet = inlineformset_factory(
            Customer, 
            Order, 
            form=OrderForm,
            fields=('product', 'quantity', 'status', 'note'),
            extra=1,
            can_delete=True
        )
        
        if request.method == "POST":
            formset = OrderFormSet(request.POST, instance=customer)
            if formset.is_valid():
                orders = formset.save(commit=False)
                valid_orders = [order for order in orders if order.product is not None]
                
                if valid_orders:
                    for order in valid_orders:
                        order.save()
                    messages.success(request, f'Заказы для клиента {customer.name} успешно созданы')
                    return redirect('customers.show', id=customer.id)
                else:
                    messages.warning(request, 'Добавьте хотя бы один заказ')
        else:
            formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
        
        return render(request, 'accounts/order_form.html', {
            'formset': formset,
            'title': 'Создать заказ',
            'customer': customer
        })
    except Customer.DoesNotExist:
        messages.error(request, 'Клиент не найден')
        return redirect('dashboard')

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def orderUpdate(request, orderId):
    try:
        order = Order.objects.get(id=orderId)
        form = OrderForm(instance=order)
        if request.method == "POST":
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, 'Заказ успешно обновлен')
                return redirect('/')
        
        return render(request, 'accounts/order_form.html', {
            'form': form,
            'title': 'Обновить заказ'
        })
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден')
        return redirect('dashboard')

@login_required(login_url='login')
@allowed_roles(roles=['admin'])
def orderDelete(request, orderId):
    try:
        order = Order.objects.get(id=orderId)
        if request.method == "POST":
            customer = order.customer
            order.delete()
            messages.success(request, f'Заказ для клиента {customer.name} успешно удален')
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('dashboard')
        return render(request, 'accounts/order_delete.html', {
            'order': order
        })
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден')
        return redirect('dashboard')

@authenticated_user
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            # Add customer group
            customer_group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(customer_group)
            
            # Create customer profile if it doesn't exist
            Customer.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,
                    'email': user.email
                }
            )
            
            messages.success(request, 'Регистрация успешно завершена! Теперь вы можете войти в систему.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {
        'form': form
    })

@authenticated_user
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').lower()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return render(request, 'accounts/login.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            
            # Determine redirect based on user group
            if user.groups.filter(name='admin').exists():
                return redirect('dashboard')
            elif hasattr(user, 'customer'):
                return redirect('customers.customer_profile')
            else:
                # If user doesn't have a customer profile, create one
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email
                )
                return redirect('customers.customer_profile')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def userLogout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('login')