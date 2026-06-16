from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.custom_logout_view, name='custom_logout'),
    path('accounts/', include('allauth.urls')),
]
