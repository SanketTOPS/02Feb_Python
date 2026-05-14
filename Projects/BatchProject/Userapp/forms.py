from django import forms
from django.contrib.auth.models import User
from .models import Note, NoteCategory

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'file', 'category', 'password']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Note Title'}),
            'description': forms.Textarea(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Note Description', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'input-field w-full p-3 rounded-lg'}),
            'file': forms.FileInput(attrs={'class': 'input-field w-full p-3 rounded-lg'}),
            'password': forms.PasswordInput(attrs={'class': 'input-field w-full p-3 rounded-lg', 'placeholder': 'Set Password (Optional)'}, render_value=True),
        }
