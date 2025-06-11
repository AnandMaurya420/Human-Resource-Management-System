from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveBalance
from User.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_leave_balance(sender,instance,created,**kwargs):
    if created:
        default_balances = {
            'SL': 8,
            'CL': 10,
            'PL': 15,
        }
    
        for leave_type, days in default_balances.items():
            LeaveBalance.objects.create(
                user = instance,
                leave_type = leave_type,
                balance = days
            )
