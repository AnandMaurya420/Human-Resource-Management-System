from django.urls import path
from .views import attendance_history,multilog_details,today_attendance_status

urlpatterns = [
    path('show/',attendance_history,name='show'),
    path('multilog_details/',multilog_details,name='multilog_details'),
    path('today_attendance_status/',today_attendance_status, name='today_attendance_status')
]