from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('approve-note/<int:note_id>/', views.approve_note, name='approve_note'),
    path('reject-note/<int:note_id>/', views.reject_note, name='reject_note'),
]
