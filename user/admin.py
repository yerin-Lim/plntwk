from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser

class CustomAdminUser(admin.ModelAdmin):
    model = CustomerUser
    fields = ['email','password','username','name','nickname','gender','birth_date']
    search_fields = ['email','username','name','nickname','gender','birth_date']
    list_display = ['email','username','name','nickname','gender','birth_date']

admin.site.register(CustomerUser, CustomAdminUser)