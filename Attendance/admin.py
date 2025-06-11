from django.contrib import admin
from .models import Attendance,Multiplelog

# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'id','date','check_in','check_out','status'
    ]

@admin.register(Multiplelog)
class MultiplelogAdmin(admin.ModelAdmin):
    list_display = [
        'id','date','check_in','check_out','total_hour'
    ]
