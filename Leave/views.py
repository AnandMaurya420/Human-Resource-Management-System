from django.shortcuts import render,redirect
from .models import LeaveRequest,LeaveBalance,CustomUser
from .forms import LeaverequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponse
from datetime import timezone,datetime
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def leave_request(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        form = LeaverequestForm(request.POST)
        if form.is_valid():
            leave_type = form.cleaned_data['leave_type']
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            days_requested = (to_date - from_date).days+1
            print('--------------------------')
            try:    
                balance = LeaveBalance.objects.get(user=user,leave_type=leave_type)
            except LeaveBalance.DoesNotExist:
                form.add_error(None, "Leave Balance not found")
                return render(request,'Leave/leave_request.html',{'form':form})

            if days_requested > balance.balance:
                form.add_error(None, f"Insufficient balance. You have only {balance.balance} days left.")
                return render(request,'Leave/leave_request.html',{'form':form})
            
            print('=============================')
            leave = form.save(commit=False)
            leave.user = user
            leave.total_days = days_requested
            leave.status = "Pending"
            print("=========save==================")
            leave.save()
            print("===========afte save===============")
            messages.success(request, "Leave request submitted")
            # return redirect('my_leave_requests')
    else:
        form = LeaverequestForm()
    return render(request,'Leave/leave_request.html',{'form':form})

@login_required
def review_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if leave.user.manager != request.user:
        return HttpResponseForbidden("You're not authorized to review this leave.")

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave.status = 'Approved'
            # Deduct leave balance
            balance = LeaveBalance.objects.get(user=leave.user, leave_type=leave.leave_type)
            if balance.balance >= leave.total_days:
                balance.balance -= leave.total_days
                balance.save()
                leave.reviewed_by = request.user
                leave.approved_on = datetime.now()
                leave.save()
            else:
                messages.error(request, "Insufficient leave balance.")
        elif action == 'reject':
            leave.status = 'Rejected'
            leave.reviewed_by = request.user
            leave.approved_on = datetime.now()
            leave.save()
        return redirect('team_leave_requests')

    return render(request, 'Leave/review_leave.html', {'leave': leave})

@login_required
def my_leave_requests(request):
    leaves = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'Leave/my_leave_request.html', {'leaves': leaves})

# @login_required
# def team_leave_requests(request):
#     # Manager views leaves of their team members
#     if  request.user.is_staff:
#         team_requests = LeaveRequest.objects.filter(user__manager=request.user, status='Pending')
#         return render(request, 'Leave/team_requests.html', {'requests': team_requests})
#     else:
#         return HttpResponse("Admins don't review leave here.")



@login_required
def team_leave_requests(request):
    print("Logged in user:", request.user.email)
    print("Team members:", request.user.team_members.all())

    if request.user.team_members.exists():
        team_requests = LeaveRequest.objects.filter(user__manager=request.user, status='Pending')
        print("Leave Requests:", team_requests)
        
        return render(request, 'Leave/team_requests.html', {'requests': team_requests})
    else:
        return HttpResponse("You are not assigned as a manager to any employees.")

# @login_required
# def team_leave_requests(request):
#     # Print logged-in user email for debug
#     print("Logged in user:", request.user.email)

#     # Print team members of the current user (should be manager)
#     team_members = request.user.team_members.all()
#     print(f"Team members count: {team_members.count()}")
#     for member in team_members:
#         print(f"Member: {member.email}")

#     # If user is manager (has team members)
#     if team_members.exists():
#         # Get pending leave requests of team members
#         team_requests = LeaveRequest.objects.filter(user__manager=request.user, status='Pending')
#         print(f"Pending leave requests count: {team_requests.count()}")

#         # Print leave requests details
#         for lr in team_requests:
#             print(f"LeaveRequest: User: {lr.user.email}, Status: {lr.status}")

#         # Pass to template
#         return render(request, 'Leave/team_requests.html', {'requests': team_requests})

#     else:
#         return HttpResponse("You are not assigned as a manager to any employees.")




