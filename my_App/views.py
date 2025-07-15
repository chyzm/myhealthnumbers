from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from my_App.utils import detectUser
from .models import User, UserProfile, HealthMetrics
from .forms import UserForm, UserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import csv




# Create your views here.

def index(request):
    # Render the index.html template
    return render(request, 'index.html')


# def registerUser(request):
#     if request.user.is_authenticated:
#         messages.warning(request, 'You are already logged in!')
#         return redirect('dashboard')
        
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password']
#             user = form.save(commit=False)
#             user.set_password(password)
#             user.role = User.CUSTOMER
#             user.is_active = True  # Activate user immediately after registration
#             user.save()
            
#             messages.success(request, 'Account created successfully!')
#             return redirect('login')  # Fixed typo from 'logregisterUserin'
#         else:
#             print(form.errors)
#     else:
#         form = UserForm()
    
#     context = {'form': form}
#     return render(request, 'registerUser.html', context)

# views.py - Update registerUser view
from django.db import transaction


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)  # Add request.FILES for file uploads
        if form.is_valid():
            password = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.is_active = True
            user.save()
            
            # Create user profile with profile picture if provided
            profile_picture = form.cleaned_data.get('profile_picture')
            if profile_picture:
                UserProfile.objects.create(
                    user=user,
                    profile_picture=profile_picture
                )
            else:
                UserProfile.objects.create(user=user)
            
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserForm()
    
    context = {'form': form}
    return render(request, 'registerUser.html', context)

# Add new view for editing profile
@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('myAccount')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'first_name': user.first_name,
    }
    return render(request, 'edit_profile.html', context)

    
   


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('calculator')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate required fields
        if not email or not password:
            messages.error(request, 'Please fill in both email and password')
            return redirect('login')
            
        # Normalize email
        email = email.lower().strip()
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Account does not exist')
            return redirect('login')
            
        # Authenticate user
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'You are now logged in!')
                return redirect('calculator')
            else:
                messages.error(request, 'Your account is not active')
        else:
            messages.error(request, 'Invalid password or email')
        
        return redirect('login')
    
    return render(request, 'login.html')

    
def logout(request): 
    auth.logout(request)
    messages.info(request, 'logged out!')
    return redirect('login')



@login_required
def calculator(request):
    if request.method == 'POST':
        try:
            # Get form data with defaults to prevent None errors
            age = int(request.POST.get('age', 0))
            weight = float(request.POST.get('weight', 0))
            height = float(request.POST.get('height', 0))
            gender = request.POST.get('gender', 'male')
            activity = float(request.POST.get('activity', 1.2))
            
            # Validate inputs
            if age <= 0 or weight <= 0 or height <= 0:
                messages.error(request, "Please enter valid values")
                return redirect('calculator')
            
            # Calculate metrics
            bmi = round(weight / ((height / 100) ** 2), 2)
            
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif bmi < 24.9:
                bmi_category = "Normal weight"
            elif bmi < 29.9:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obese"
            
            bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == 'male' else -161)
            tdee = round(bmr * activity, 2)
            
            ibw = 50 + 0.9 * (height - 152) if gender == 'male' else 45.5 + 0.9 * (height - 152)
            ibw_min = round(ibw * 0.9, 2)
            ibw_max = round(ibw * 1.1, 2)
            ibw_range = f"{ibw_min} kg - {ibw_max} kg"
            
            mhr = 220 - age
            
            # Save to database
            metrics = HealthMetrics.objects.create(
                user=request.user,
                age=age,
                weight=weight,
                height=height,
                gender=gender,
                activity_level=activity,
                bmi=bmi,
                bmi_category=bmi_category,
                bmr=bmr,
                tdee=tdee,
                ibw=ibw_range,
                mhr=mhr
            )
            
            # Update profile with latest metrics
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.latest_metrics = metrics
            profile.save()
            
            return redirect('result', metrics_id=metrics.id)
            
        except (ValueError, TypeError):
            messages.error(request, "Invalid input values")
            return redirect('calculator')
    
    # For GET requests
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    
    context = {
        'first_name': request.user.first_name,
        'profile_picture': profile.profile_picture.url if profile and profile.profile_picture else None
    }
    return render(request, 'calculator.html', context)



   
  


def dashboard(request):
    # Render the calculate.html template
    
    context = {
        'first_name': request.user.first_name,  # Pass the logged-in user's first name
    }
    return render(request, 'dashboard.html', context)





# My Account

@login_required
def health_history(request):
    # Get all health metrics for the current user, ordered by date
    health_metrics = request.user.health_metrics.all().order_by('-created_at')
    
    context = {
        'health_metrics': health_metrics,
    }
    return render(request, 'health_history.html', context)




@login_required
def my_account(request):
    return render(request, 'my_account.html')

@login_required
def change_password(request):
    """
    Handles password change functionality for authenticated users.
    Uses Django's built-in PasswordChangeForm for validation.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('myAccount')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'first_name': request.user.first_name,
    }
    return render(request, 'change_password.html', context)




@login_required
def delete_account(request):
    """
    Handles account deletion with confirmation.
    Requires POST method to prevent accidental deletion via GET requests.
    """
    if request.method == 'POST':
        # Delete user account after confirmation
        request.user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('login')
    
    # For GET requests, show confirmation page
    context = {
        'first_name': request.user.first_name,
    }
    return render(request, 'delete_account.html', context)




@login_required
def download_results(request):
    """
    Generates a CSV file of the user's health metrics history.
    Returns the file as a downloadable attachment.
    """
    # Get all health metrics for the current user
    health_metrics = HealthMetrics.objects.filter(user=request.user).order_by('-created_at')
    
    if not health_metrics.exists():
        messages.warning(request, 'No health metrics found to download.')
        return redirect('healthHistory')
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="health_metrics_history.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow([
        'Date', 'Age', 'Weight (kg)', 'Height (cm)', 'Gender', 
        'Activity Level', 'BMI', 'BMI Category', 'BMR', 'TDEE', 
        'Ideal Weight Range', 'Max Heart Rate'
    ])
    
    # Write data rows
    for metric in health_metrics:
        writer.writerow([
            metric.created_at.strftime('%Y-%m-%d %H:%M'),
            metric.age,
            metric.weight,
            metric.height,
            metric.gender.capitalize(),
            metric.activity_level,
            metric.bmi,
            metric.bmi_category,
            metric.bmr,
            metric.tdee,
            metric.ibw,
            metric.mhr
        ])
    
    return response

# For dashboard
@login_required(login_url='login')
def customerDashboard(request):
     return render(request, 'accounts/customerDashboard.html')
 
 
 
 # views.py
# @login_required
# def result_view(request, metrics_id):
#     metrics = get_object_or_404(HealthMetrics, id=metrics_id, user=request.user)
#     return render(request, 'result.html', {'metrics': metrics})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import HealthMetrics
import json
from django.core.serializers.json import DjangoJSONEncoder

def result_view(request, metrics_id):
    metrics = get_object_or_404(HealthMetrics, id=metrics_id, user=request.user)
    history = request.user.health_metrics.order_by('created_at')

    chart_data = {
        'dates': [entry.created_at.strftime('%Y-%m-%d') for entry in history],
        'bmi': [float(entry.bmi) for entry in history],
        'bmr': [float(entry.bmr) for entry in history],
        'tdee': [float(entry.tdee) for entry in history],
        'mhr': [float(entry.mhr) for entry in history]
    }

    return render(request, 'result.html', {
        'metrics': metrics,
        'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder)
    })
    
    

import json
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

@login_required
def health_chart_view(request):
    history = request.user.health_metrics.order_by('created_at')
    chart_data = {
        'dates': [m.created_at.strftime('%Y-%m-%d') for m in history],
        'bmi': [m.bmi for m in history],
        'bmr': [m.bmr for m in history],
        'tdee': [m.tdee for m in history],
        'mhr': [m.mhr for m in history],
    }
    return render(request, 'health_chart.html', {
        'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder)
    })

