from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import RegistrationForm


def home(request):
    tiles = [
        {
            'icon': '01',
            'value': 'Fast',
            'title': 'Modern Websites',
            'description': 'Responsive websites designed to look amazing on every device.',
            'color': '#2563eb',
        },
        {
            'icon': '02',
            'value': 'Secure',
            'title': 'Reliable Systems',
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
    ]
    return render(request, 'home.html', {'tiles': tiles})

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
    # Replace these static values with database queries (e.g., Order.objects.count())
    tiles = [
        {
            "title": "Monthly Visitors",
            "value": "24,500",
            "subtitle": "+12% vs last month",
            "badge_color": "success",
        },
        {
            "title": "Today's Revenue",
            "value": "KES 145,000",
            "subtitle": "14 completed orders",
            "badge_color": "primary",
        },
        {
            "title": "New Inquiries",
            "value": "18",
            "subtitle": "5 unread messages",
            "badge_color": "warning",
        },
        {
            "title": "Open Support Tickets",
            "value": "5",
            "subtitle": "2 high priority",
            "badge_color": "danger",
        },
    ]

    return render(request, "dashboard.html", {"tiles": tiles})

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
    return render(request, 'dashboard.html')
