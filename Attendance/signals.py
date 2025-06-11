from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from .models import Attendance,Multiplelog
from User.models import CustomUser
from django.utils.timezone import now

@receiver(user_logged_in)
def mark_attendance_on_login(sender, request, user, **kwargs):
    today = now().date()
    current_time = now().time()

    attendance, created = Attendance.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'status': 'Present',
            'check_in': current_time
        }
    )
    # Update check-in if accidentally not recorded
    if not created and attendance.check_in is None:
        attendance.check_in = current_time
        attendance.save()

# user_logged_in.connect(mark_attendance_on_login,sender=CustomUser)   # you can use in place of @receiver(user_logged_in),, both ok

@receiver(user_logged_out)
def mark_attendance_on_logout(sender, request, user, **kwargs):

    today = now().date()
    current_time = now().time()

    try:
        attendance = Attendance.objects.get(user=user, date=today)
        attendance.check_out = current_time
        attendance.save()
    except Attendance.DoesNotExist:
        # Edge case: if somehow login wasn't tracked
        Attendance.objects.create(
            user=user,
            date=today,
            status='Present',
            check_out=current_time
        )


# -----------------------------------------------------------------------------------------------------

@receiver(user_logged_in)
def auto_check_in(sender, request, user, **kwargs):
    # today = now().date()

    # # Create or get today's log
    # attendance, created = Multiplelog.objects.get_or_create(
    #     user=user,
    #     date=today,
    #     defaults={'check_in': now()}
    # )

    # # If log exists but check_in is still empty, fill it
    # if not created and not attendance.check_in:
    #     attendance.check_in = now()
    #     attendance.save()
    # else:
    #     entry = Multiplelog.objects.create(        
    #     user=user,
    #     date=today,
    #     check_in =now()
    #     )
    #     entry.save()

    today = now().date()

    # Check if there's already an open session (no checkout)
    open_session = Multiplelog.objects.filter(
        user=user,
        date=today,
        check_out__isnull=True
    ).first()

    if not open_session:
        # No open session → create new check-in
        Multiplelog.objects.create(
            user=user,
            date=today,
            check_in=now()
        )

@receiver(user_logged_out)
def auto_check_out(sender, request, user, **kwargs):
    today = now().date()
    try:
        # attendance = Multiplelog.objects.get(user=user, date=today)
        # if not attendance.check_out:
        #     attendance.check_out = now()
        #     attendance.save()
        # else:
        #     entry = Multiplelog.objects.create(        
        #     user=user,
        #     date=today,
        #     check_out= now()
        #     )
        #     entry.save()

                # Get the latest open session (no check-out yet)
        session = Multiplelog.objects.filter(
            user=user,
            date=today,
            check_out__isnull=True
        ).latest('check_in')

        session.check_out = now()
        session.save()

    except Multiplelog.DoesNotExist:
        # Edge case: if somehow login wasn't tracked
        Multiplelog.objects.create(
            user=user,
            date=today,
            check_out= now()
        )