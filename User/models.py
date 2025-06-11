from django.db import models
from User.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):

    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('MKT', 'Marketing'),
        ('SALES', 'Sales'),
        ('SUPPORT', 'Customer Support'),
        ('ADMIN', 'Administration'),
        ('IT', 'Information Technology'),
        ('QA', 'Quality Assurance'),
        
    ]

    DESIGNATION_CHOICES = [
        ('INTERN', 'Intern'),
        ('SRE', 'Software Engineer'),
        ('SSE', 'Senior Software Engineer'),
        ('TL', 'Team Lead'),
        ('PM', 'Project Manager'),
        ('HRM', 'HR Manager'),
        ('BA', 'Business Analyst'),
        ('QA', 'QA Engineer'),
        ('SALES_EX', 'Sales Executive'),
        ('SUPPORT_EX', 'Support Executive'),
        ('FIN_ANALYST', 'Financial Analyst'),
        ('ADMIN', 'Administrator'),
        ('CEO', 'Chief Executive Officer'),
    ]

    
    employee_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES )
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='team_members')
    joining_date = models.DateField(null=True, blank=True,auto_now_add=True)
    
    # reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    # employment_type = models.CharField(max_length=20, choices=[
    #     ('Full-Time', 'Full-Time'),
    #     ('Part-Time', 'Part-Time'),
    #     ('Contract', 'Contract')
    # ], default='Full-Time')

    # Required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'employee_id']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.employee_id})"