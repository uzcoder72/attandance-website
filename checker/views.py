from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student

def login_view(request):
    # If already logged in, go straight to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    error_message = None
    
    if request.method == 'POST':
        # Get username and password from the HTML form
        user_param = request.POST.get('username')
        pass_param = request.POST.get('password')
        
        # Check against our database (admin, admin123)
        user = authenticate(request, username=user_param, password=pass_param)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password"
            
    return render(request, 'checker/login.html', {'error': error_message})

@login_required(login_url='login')
def dashboard_view(request):
    # Get all students and calculate their attendance
    students = Student.objects.all()
    
    attendance_data = []
    
    for student in students:
        # Get all attendance records for this student
        records = student.attendance_set.all()
        total_classes = records.count()
        
        if total_classes > 0:
            present_classes = records.filter(is_present=True).count()
            # Calculate percentages
            present_percentage = round((present_classes / total_classes) * 100, 2)
            absent_percentage = round(100 - present_percentage, 2)
        else:
            present_percentage = 0
            absent_percentage = 0
            
        attendance_data.append({
            'student': student,
            'present_pct': present_percentage,
            'absent_pct': absent_percentage,
        })
        
    context = {
        'attendance_data': attendance_data
    }
    
    return render(request, 'checker/dashboard.html', context)

def custom_logout(request):
    logout(request)
    return redirect('login')
