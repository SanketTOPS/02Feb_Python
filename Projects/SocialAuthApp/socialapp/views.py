from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def home_view(request):
    """Landing page view – renders the gradient home template."""
    return render(request, 'home.html')

@login_required
def dashboard_view(request):
    """Protected dashboard showing user info and connected accounts."""
    return render(request, 'dashboard.html')

def custom_logout_view(request):
    """Logs the user out and redirects to the home page."""
    logout(request)
    return redirect('home')
