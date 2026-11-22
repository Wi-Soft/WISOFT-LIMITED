from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm


def home(request):
    from django.contrib import messages
    from django.db.models import Avg, Count
    from .models import PortfolioRating

    if request.method == 'POST' and request.user.is_authenticated:
        try:
            rating = int(request.POST.get('rating', 0))
        except (TypeError, ValueError):
            rating = 0

        if 1 <= rating <= 5:
            PortfolioRating.objects.update_or_create(
                user=request.user,
                defaults={
                    'rating': rating,
                    'comment': request.POST.get('comment', '').strip(),
                },
            )
            messages.success(request, 'Thank you for rating WISOFT LIMITED.')
            return redirect('home')

        messages.error(request, 'Please select a rating between 1 and 5.')

    rating_stats = PortfolioRating.objects.aggregate(average=Avg('rating'), total=Count('id'))
    rating_average = rating_stats['average'] or 0
    rating_count = rating_stats['total']
    user_rating = None
    if request.user.is_authenticated:
        user_rating = PortfolioRating.objects.filter(user=request.user).first()

    tiles = [
        {
            'icon': '00',
            'value': 'Staff',
            'title': 'Professional Team',
            'description': 'Our team is composed of highly skilled professionals dedicated to delivering top-notch services.',
            'color': '#f59e0b',
        },
        {
            'icon': '01',
            'value': 'Fast',
            'title': 'Modern Tiles',
            'description': 'We have modern tiles for your house.',
            'color': '#2563eb',
        },
        {
            'icon': '02',
            'value': 'Secure',
            'title': 'Reliable Tiles',
            'description': 'Stable and secure applications built for long-term business growth.',
            'color': '#7c3aed',
        },
        {
            'icon': '03',
            'value': 'Smart',
            'title': 'Digital Solutions',
            'description': 'Creative tools that automate work and improve customer experiences.',
            'color': '#059669',
        },
        {
            'icon': '04',
            'value': '24/7',
            'title': 'Dedicated Support',
            'description': 'Friendly technical support when you need help or need a new feature.',
            'color': '#ea580c',
        },
        {
            'icon': '05',
            'value': 'Affordable',
            'title': 'Cost-Effective Solutions',
            'description': 'We provide cost-effective solutions for your business needs.',
            'color': '#d97706',
        },
        {
            'icon': '06',
            'value': 'Customizable',
            'title': 'Tailored Solutions',
            'description': 'We offer customizable solutions to meet your specific requirements.',
            'color': '#db2777',
        },
        {
            'icon': '07',
            'value': 'Innovative',
            'title': 'Cutting-Edge Technology',
            'description': 'We leverage the latest technology to deliver innovative solutions.',
            'color': '#f43f5e',
        },
        {
            'icon': '08',
            'value': 'Collaborative',
            'title': 'Team-Oriented Approach',
            'description': 'We work closely with our clients to ensure their success.',
            'color': '#8b5cf6',
        }
    ]
    return render(request, 'home.html', {
        'tiles': tiles,
        'rating_average': rating_average,
        'rating_count': rating_count,
        'user_rating': user_rating,
    })

def fooder(request):
    return render(request, 'fooder.html')

def about(request):
    return render(request, 'About.html')


def services(request):
    return render(request, 'Services.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return redirect('dashboard')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'An account with that email address already exists.')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['full_name'],
                )
                login(request, user)
                return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next', 'dashboard'))
    else:
        form = AuthenticationForm(request)
    return render(request, 'signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='signin')
def dashboard(request):
    from django.db.models import Sum
    from .models import Category, Product, StockMovement

    total_tiles = Product.objects.count()
    total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
    low_stock_count = sum(1 for product in Product.objects.all() if product.is_low_stock)
    total_categories = Category.objects.count()
    sales = StockMovement.objects.filter(movement_type='OUT')
    total_sales = sales.aggregate(total=Sum('quantity'))['total'] or 0
    total_orders = sales.count()
    total_revenue = sum(order.total_amount for order in sales.select_related('product'))
    total_workers = User.objects.count()

    tiles = [
        {'title': 'Tile Products', 'value': f'{total_tiles}', 'subtitle': 'Admin-added tile products', 'badge_color': 'primary'},
        {'title': 'Tiles Sold', 'value': f'{total_sales}', 'subtitle': 'Total units sold', 'badge_color': 'success'},
        {'title': 'Sales Orders', 'value': f'{total_orders}', 'subtitle': 'Completed sales movements', 'badge_color': 'info'},
        {'title': 'Sales Revenue', 'value': f'KES {total_revenue:,.2f}', 'subtitle': 'Total order value', 'badge_color': 'success'},
        {'title': 'Workers', 'value': f'{total_workers}', 'subtitle': 'Registered users', 'badge_color': 'warning'},
        {'title': 'Stock on Hand', 'value': f'{total_stock}', 'subtitle': 'Available units', 'badge_color': 'danger'},
        {'title': 'Low Stock', 'value': f'{low_stock_count}', 'subtitle': 'Products needing attention', 'badge_color': 'danger'},
        {'title': 'Categories', 'value': f'{total_categories}', 'subtitle': 'Tile categories', 'badge_color': 'secondary'},
    ]
    return render(request, 'dashboard.html', {'tiles': tiles})

@login_required(login_url='signin')
def order(request):
    from django.urls import reverse
    from django.contrib import messages
    from .models import Product, StockMovement

    selected_product = None

    product_id = request.GET.get('product') or request.GET.get('tile') or request.POST.get('product')
    ordered_quantity = request.GET.get('quantity')

    try:
        ordered_quantity = int(ordered_quantity) if ordered_quantity else 1
    except (TypeError, ValueError):
        ordered_quantity = 1

    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)
        request.session['selected_product_id'] = selected_product.id
    else:
        selected_product_id = request.session.get('selected_product_id')
        if selected_product_id:
            selected_product = Product.objects.filter(id=selected_product_id).first()
        if not selected_product:
            selected_product = Product.objects.order_by('-created_at').first()

    if request.method == 'POST':
        product = get_object_or_404(Product, id=request.POST.get('product'))
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 0

        if quantity < 1:
            messages.error(request, 'Please enter a valid quantity.')
        elif quantity > product.stock:
            messages.error(request, f'Only {product.stock} units are available.')
        else:
            product.stock -= quantity
            product.save(update_fields=['stock'])
            StockMovement.objects.create(
                product=product,
                movement_type='OUT',
                quantity=quantity,
                note=f'Order placed by {request.user.username}',
            )
            messages.success(request, 'Your tile order was placed successfully.')
            return redirect(f"{reverse('order')}?product={product.id}&ordered=1")

        selected_product = product

    orders = StockMovement.objects.select_related('product').filter(
        movement_type='OUT'
    ).order_by('-created_at')

    return render(request, 'Order.html', {
        'selected_product': selected_product,
        'ordered_quantity': ordered_quantity,
        'selected_total': selected_product.price * ordered_quantity if selected_product else 0,
        'orders': orders,
    })


@login_required(login_url='signin')
def orders(request):
    from .models import StockMovement

    orders = StockMovement.objects.select_related('product').all().order_by('-created_at')
    return render(request, 'Order.html', {'orders': orders})

def buy(request):
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from .models import Product, StockMovement

    if request.method == 'POST':
        product = get_object_or_404(Product, id=request.POST.get('product'))

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 0

        if quantity < 1:
            messages.error(request, 'Please enter a valid quantity.')
        elif quantity > product.stock:
            messages.error(request, f'Only {product.stock} units of this tile are available.')
        else:
            product.stock -= quantity
            product.save(update_fields=['stock'])
            StockMovement.objects.create(
                product=product,
                movement_type='OUT',
                quantity=quantity,
                note='Customer tile order from Buy page',
            )
            total = product.price * quantity
            messages.success(
                request,
                f'You have ordered successfully. Total: KSh {total}. Wait as the company processes your order.',
            )
            request.session['selected_product_id'] = product.id

            return redirect('buy')

    products = Product.objects.select_related('category').all().order_by('-created_at')
    search = request.GET.get('q', '').strip()

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'Buy.html', {'products': products, 'search': search})