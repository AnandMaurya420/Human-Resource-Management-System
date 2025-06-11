from django.urls import path
from .views import leave_request, review_leave,my_leave_requests,team_leave_requests

urlpatterns = [
    path('leave_request/',leave_request,name='leave_request'),
    path('review_leave/<int:leave_id>/',review_leave,name='review_leave'),
    path('my_leave_requests/',my_leave_requests,name='my_leave_requests'),
    path('team_leave_requests/',team_leave_requests,name='team_leave_requests'),
   
]
