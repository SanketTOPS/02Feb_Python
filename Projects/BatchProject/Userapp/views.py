import random
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import SignupForm, NoteForm
from .models import Profile, Note, NoteCategory

def home_view(request):
    return render(request, 'Userapp/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False # Deactivate until OTP verified
            user.save()
            
            otp = str(random.randint(100000, 999999))
            Profile.objects.create(user=user, otp=otp)
            
            # Send OTP Email
            subject = 'Your NotesVault OTP Verification Code'
            html_message = render_to_string('Userapp/otp_email.html', {'otp': otp})
            plain_message = strip_tags(html_message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
            
            request.session['unverified_user_id'] = user.id
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_otp')
    else:
        form = SignupForm()
    return render(request, 'Userapp/signup.html', {'form': form})

def verify_otp_view(request):
    user_id = request.session.get('unverified_user_id')
    if not user_id:
        return redirect('signup')
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            if profile.otp == otp_entered:
                user.is_active = True
                user.save()
                profile.is_verified = True
                profile.otp = None
                profile.save()
                login(request, user)
                del request.session['unverified_user_id']
                messages.success(request, 'Account verified successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid OTP.')
        except User.DoesNotExist:
            return redirect('signup')
            
    return render(request, 'Userapp/verify_otp.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('dashboard')
    else:
        form = NoteForm()
    
    return render(request, 'Userapp/dashboard.html', {'notes': notes, 'form': form})

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Please verify your email first.')
                request.session['unverified_user_id'] = user.id
                return redirect('verify_otp')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'Userapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        
        if user:
            otp = str(random.randint(100000, 999999))
            profile, created = Profile.objects.get_or_create(user=user)
            profile.otp = otp
            profile.save()
            
            # Send OTP Email
            subject = 'Password Reset OTP - NotesVault'
            html_message = render_to_string('Userapp/reset_otp_email.html', {'otp': otp})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
            
            request.session['reset_user_id'] = user.id
            messages.success(request, 'Password reset OTP sent to your email.')
            return redirect('reset_password_verify')
        else:
            messages.error(request, 'User with this username or email does not exist.')
            
    return render(request, 'Userapp/forgot_password.html')

def reset_password_verify_otp_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        try:
            user = User.objects.get(id=user_id)
            if user.profile.otp == otp_entered:
                request.session['reset_verified'] = True
                user.profile.otp = None
                user.profile.save()
                messages.success(request, 'OTP verified. You can now reset your password.')
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP.')
        except User.DoesNotExist:
            return redirect('forgot_password')
            
    return render(request, 'Userapp/reset_password_verify_otp.html')

def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    verified = request.session.get('reset_verified')
    
    if not user_id or not verified:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        new_pass = request.POST.get('new_password')
        conf_pass = request.POST.get('confirm_password')
        
        if new_pass == conf_pass:
            user = User.objects.get(id=user_id)
            user.set_password(new_pass)
            user.save()
            
            # Clear session
            del request.session['reset_user_id']
            del request.session['reset_verified']
            
            messages.success(request, 'Password reset successful. Please login with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'Userapp/reset_password.html')

def about_view(request):
    return render(request, 'Userapp/about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject_text = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        # Send Thank You Email to User
        subject = f"Thank you for contacting NotesVault: {subject_text}"
        context = {
            'name': name,
            'subject': subject_text
        }
        html_message = render_to_string('Userapp/thank_you_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)
        
        # Optionally send notification to admin (using same host user as receiver for demo)
        admin_subject = f"New Contact Form Submission: {subject_text}"
        admin_message = f"Name: {name}\nEmail: {email}\nSubject: {subject_text}\nMessage: {message_text}"
        send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        
        messages.success(request, 'Thank you! Your message has been sent. Check your email for confirmation.')
        return redirect('contact')
        
    return render(request, 'Userapp/contact.html')

def unlock_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    # Check if user already has access via session
    if not note.password or request.session.get(f'unlocked_note_{note.id}'):
        return render(request, 'Userapp/view_note.html', {'note': note})
        
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == note.password:
            # Grant temporary access via session
            request.session[f'unlocked_note_{note.id}'] = True
            return render(request, 'Userapp/view_note.html', {'note': note})
        else:
            messages.error(request, 'Incorrect password. Access denied.')
            
    return render(request, 'Userapp/unlock_note.html', {'note': note})
