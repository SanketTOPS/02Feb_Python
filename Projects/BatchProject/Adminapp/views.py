from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from Userapp.models import Note, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

@staff_member_required(login_url='admin_login')
def admin_dashboard(request):
    total_users = User.objects.count()
    total_notes = Note.objects.count()
    users = User.objects.all().order_by('-date_joined')
    recent_notes = Note.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_notes': total_notes,
        'users': users,
        'recent_notes': recent_notes,
    }
    return render(request, 'Adminapp/dashboard.html', context)

@staff_member_required(login_url='admin_login')
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        messages.error(request, "Cannot block an admin user.")
    else:
        user.is_active = False
        user.save()
        messages.success(request, f"User {user.username} has been blocked.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='admin_login')
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"User {user.username} has been unblocked.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='admin_login')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        messages.error(request, "Cannot delete an admin user.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='admin_login')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "User details updated.")
        return redirect('admin_dashboard')
    return render(request, 'Adminapp/edit_user.html', {'target_user': user})

@staff_member_required(login_url='admin_login')
def approve_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.status = 'Approved'
    note.save()
    
    # Send Email
    subject = f"Note Approved: {note.title}"
    context = {
        'note': note,
        'status': 'Approved',
        'dashboard_url': request.build_absolute_uri('/dashboard/')
    }
    html_message = render_to_string('Userapp/note_status_email.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [note.user.email], html_message=html_message)
    
    messages.success(request, f"Note '{note.title}' has been approved.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='admin_login')
def reject_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.status = 'Rejected'
    note.save()
    
    # Send Email
    subject = f"Note Rejected: {note.title}"
    context = {
        'note': note,
        'status': 'Rejected'
    }
    html_message = render_to_string('Userapp/note_status_email.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [note.user.email], html_message=html_message)
    
    messages.warning(request, f"Note '{note.title}' has been rejected.")
    return redirect('admin_dashboard')

def admin_login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back, Administrator {user.username}!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Only staff members can access the Admin Dashboard.")
        else:
            messages.error(request, "Invalid admin credentials.")
    return render(request, 'Adminapp/admin_login.html')

def admin_logout_view(request):
    logout(request)
    messages.info(request, "Admin logged out successfully.")
    return redirect('admin_login')
