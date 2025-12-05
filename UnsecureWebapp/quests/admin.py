from django.contrib import admin

from .models import Quest, Choice

# Register your models here.
admin.site.register(Quest)
admin.site.register(Choice)