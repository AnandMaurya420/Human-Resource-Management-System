from django.shortcuts import render,redirect
from .models import CustomUser
from .forms import CustomUserCreationForm,UserEditDashboard
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# Create your views here.

def user_register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User register successfully")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request,'User/user_register.html', {'form': form})

def user_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(email,password)
            user = authenticate(request,username=email,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,'login successfully')
                return redirect('dashboard')
            else:
                messages.error(request,'Invalid Email or Password')

    else:
        form = AuthenticationForm()
    return render(request, 'User/user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    # print(request.user)
    # return render(request, 'User/user_dashboard.html',{'user': request.user})
    return render(request, 'User/dashboard.html',{'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    print(user.designation)
    if user.designation != 'HRM':
        return HttpResponseForbidden("You are not allowed to edit this information.")
    if request.method == 'POST':
        form = UserEditDashboard(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserEditDashboard(instance=user)
    return render(request,'User/edit_profile.html',{'form':form})

@login_required
def user_profile_info(request):
    # Logged-in user
    user = request.user
    return render(request, 'User/user_profile.html', {'user': user})

# @login_required
# def user_dashboard(request):
#     user = request.user
#     can_edit = user.role == 'HR'  # Check if role is HR

#     return render(request, 'User/user_dashboard.html', {
#         'user': user,
#         'can_edit': can_edit
#     })

