from django.db import models
from User.models import CustomUser

# Create your models here.

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
        ('PL', 'Paid Leave'),
        ('LOP', 'Leave Without Pay'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    total_days = models.IntegerField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='leave_docs/', null=True, blank=True)
    reviewed_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_leaves')


    def __str__(self):
        return f"{self.user.email} - {self.leave_type} ({self.status})"
    
    # @property
    # def total_days(self):
    #     return (self.to_date - self.from_date).days + 1
    
    # @property
    # def available_balance(self):
    #     from .models import LeaveBalance
    #     try:
    #         balance = LeaveBalance.objects.get(user=self.user, leave_type=self.leave_type)
    #         return balance.balance
    #     except LeaveBalance.DoesNotExist:
    #         return 0

class LeaveBalance(models.Model):
    LEAVE_TYPES = [
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
        ('PL', 'Paid Leave'),
        ('LOP', 'Leave Without Pay'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.leave_type}: {self.balance} days"