from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Task
from .forms import TaskForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def contact_us(request):
    return render(request,'contact_us.html' )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')  # Redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'  # Add custom context variables if needed
        return context

def index(request):
    return render(request, 'index.html')


@login_required
def profile_view(request):
    """
    Render the profile page for the logged-in user.
    """
    return render(request, 'profile.html', {'user': request.user})


from datetime import date
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by('priority', 'deadline')

    # Categorize tasks
    today = date.today()
    upcoming_tasks = tasks.filter(deadline__gte=today)
    past_due_tasks = tasks.filter(deadline__lt=today)

    # Organize by priority
    def categorize_by_priority(tasks):
        return {
            'High': tasks.filter(priority='high'),
            'Medium': tasks.filter(priority='medium'),
            'Low': tasks.filter(priority='low'),
        }

    categorized_upcoming = categorize_by_priority(upcoming_tasks)
    categorized_past_due = categorize_by_priority(past_due_tasks)

    context = {
        'categorized_upcoming': categorized_upcoming,
        'categorized_past_due': categorized_past_due,
    }
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_details(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    return render(request, 'task_details.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')
@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'update_task.html', {'form': form, 'task': task})

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('index')  # Redirect to the home page or login page
    return render(request, 'profile.html')

from .models import Profile

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        picture = request.FILES.get('picture')
        if picture:
            profile = request.user.profile
            profile.picture = picture
            profile.save()
            return redirect('profile')  # Redirect back to the profile page
    return render(request, 'profile.html')

from datetime import date


