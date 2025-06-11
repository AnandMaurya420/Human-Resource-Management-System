from django.shortcuts import render
from .forms import AttendanceForm
from .models import Attendance,Multiplelog
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import date

# Create your views here.

@login_required
def attendance_history(request):
    selected_date = request.GET.get('date')
    
    # Filter by date if provided
    if selected_date:
        records = Attendance.objects.filter(user=request.user, date=selected_date).order_by('-date')
    else:
        records = Attendance.objects.filter(user=request.user).order_by('-date')

    # Pagination (10 records per page)
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Attendance/attendance.html', {
        'page_obj': page_obj,
        'selected_date': selected_date,
    })

@login_required
def today_attendance_status(request):
    today_status = Attendance.objects.get(user=request.user, date=date.today())
    print("------->",today_status.check_in)
    print("------->",today_status.status)
    print("------->",today_status.date)
    print("------->",today_status.check_out)
    return render(request, 'Attendance/today_attendance.html', {'today_status': today_status })

# @login_required
# def multilog_details(request):
#     today = timezone.now().date()  # Get current date
#     multilog_history = Multiplelog.objects.filter(user=request.user, date=today).order_by('-date')
#     return render(request, 'Attendance/multilog_detail.html', {'multilog_history': multilog_history})

@login_required
def multilog_details(request):
    selected_date = request.GET.get('date')
    if selected_date:
        multilog_history = Multiplelog.objects.filter(user=request.user, date=selected_date)
    else:
        today = timezone.now().date()
        multilog_history = Multiplelog.objects.filter(user=request.user, date=today)
    
    return render(request, 'Attendance/multilog_detail.html', {'multilog_history': multilog_history})