from django.db import models
from User.models import CustomUser

# Create your models here.

class Attendance(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Present','Present'),('Absent','Absent'),('Leave','Leave')])

    class Meta:
        unique_together = ('user', 'date')  # prevent multiple entries per day

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.status}"

class Multiplelog(models.Model):

    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    total_hour = models.DurationField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            self.total_hour = self.check_out - self.check_in
        super().save(*args, **kwargs)
