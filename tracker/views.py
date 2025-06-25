from django.shortcuts import render, redirect
from .models import Task, WorkReport, PendingRegistration
from .forms import EmployerRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Secure password
            user.is_active = False  # Require admin approval
            user.save()

            # Save to pending list (assuming model exists)
            PendingRegistration.objects.create(user=user)

            messages.success(request, 'Registration submitted. Awaiting admin approval.')
            return redirect('login')
    else:
        form = EmployerRegistrationForm()

    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Your account is pending approval by the admin.')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_tasks = Task.objects.filter(assigned_to=request.user)
    user_reports = WorkReport.objects.filter(user=request.user).order_by('-timestamp')

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        report_text = request.POST.get('report_text')
        report_file = request.FILES.get('report_file')  # Get uploaded file

        task = Task.objects.get(id=task_id)

        WorkReport.objects.create(
            task=task,
            user=request.user,
            report_text=report_text,
            report_file=report_file
        )

        messages.success(request, 'Report submitted successfully.')
        return redirect('dashboard')

    return render(request, 'dashboard.html', {
        'tasks': user_tasks,
        'reports': user_reports
    })

@staff_member_required
def all_reports(request):
    reports = WorkReport.objects.select_related('task', 'user').order_by('-timestamp')
    return render(request, 'all_reports.html', {'reports': reports})
