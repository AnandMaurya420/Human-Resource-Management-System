from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label ='Confirm-Password', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ['email', 'employee_id', 'first_name', 'last_name', 'phone_number','manager','gender','date_of_birth','address','department',
                  'designation','profile_picture']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered")
        return email
    
    def clean_password2(self):
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if  pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Password do not match")
        return pwd2
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user

class UserEditDashboard(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'employee_id', 'first_name', 'last_name', 'phone_number','manager','gender','date_of_birth','address','department',
                  'designation','profile_picture']
