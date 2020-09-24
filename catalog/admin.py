from django.contrib import admin

# Register your models here.
from .models import User, Class#Author, Genre, Book, BookInstance, 

# Register the user
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name','email','status','card_number','password')

# Register the classes
@admin.register(Class) 
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'topic','tutor','student','pay_per_hour')
