from django.contrib import admin
from .models import Comment, Recommendation

# Register your models here.

admin.site.register(Comment)
admin.site.register(Recommendation)