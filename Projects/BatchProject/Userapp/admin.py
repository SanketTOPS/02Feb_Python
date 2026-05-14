from django.contrib import admin
from .models import Profile, NoteCategory, Note

admin.site.register(Profile)
admin.site.register(NoteCategory)
admin.site.register(Note)
