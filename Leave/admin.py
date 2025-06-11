from django.contrib import admin
from .models import LeaveBalance, LeaveRequest
# Register your models here.

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):

    list_display = [
        'id','user','leave_type','from_date','to_date','total_days','reason','status','applied_on','approved_on','attachment','reviewed_by'
    ]

@admin.register(LeaveBalance)
class LeaveRequestAdmin(admin.ModelAdmin):

    list_display = [
        'id','user','leave_type','balance'
    ]