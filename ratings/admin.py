from django.contrib import admin
from .models import Ratings
# Register your models here.
@admin.register(Ratings)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','user','comment']