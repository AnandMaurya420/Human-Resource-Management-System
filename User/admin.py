from django.contrib import admin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustemuserAdmin(admin.ModelAdmin):
    list_display = [
        'id','employee_id','first_name','last_name','email','phone_number','date_of_birth','address','profile_picture','department',
        'designation','manager'
    ]
    search_fields = ('email','employee_id','first_name','last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'address', 'profile_picture')}),
        ('Employment Details', {'fields': ('employee_id', 'department', 'designation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'employee_id', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

