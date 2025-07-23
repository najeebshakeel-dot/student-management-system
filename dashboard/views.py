    # dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate # For authentication functions
from django.contrib import messages # For displaying messages to the user
from .forms import LoginForm # Import our login form
from .models import User, Professor, Student, College # Import our models

    # --- Helper functions for checking user types ---
    # These decorators will be used to restrict access to certain views.
def is_super_admin(user):
        return user.is_authenticated and user.user_type == 'super_admin'

def is_college_admin(user):
        return user.is_authenticated and user.user_type == 'college_admin'

def is_professor(user):
        return user.is_authenticated and user.user_type == 'professor'

def is_student(user):
        return user.is_authenticated and user.user_type == 'student'

    # --- Authentication Views ---

def user_login(request):
        # If the user is already logged in, redirect them to their respective dashboard
        if request.user.is_authenticated:
            if request.user.user_type == 'super_admin':
                return redirect('admin:index') # Redirect to Django admin
            elif request.user.user_type == 'college_admin':
                return redirect('college_admin_dashboard') # To be created later
            elif request.user.user_type == 'professor':
                return redirect('professor_dashboard')
            elif request.user.user_type == 'student':
                return redirect('student_dashboard')

        if request.method == 'POST':
            # If the form is submitted (POST request)
            form = LoginForm(request.POST) # Create a form instance with submitted data
            if form.is_valid(): # Check if the submitted data is valid
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # Authenticate the user against Django's authentication system
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # If authentication is successful, log the user in
                    login(request, user)
                    messages.success(request, f"Welcome, {user.username}!") # Display a success message
                    # Redirect based on user type
                    if user.user_type == 'super_admin':
                        return redirect('admin:index')
                    elif user.user_type == 'college_admin':
                        return redirect('college_admin_dashboard') # To be created later
                    elif user.user_type == 'professor':
                        return redirect('professor_dashboard')
                    elif user.user_type == 'student':
                        return redirect('student_dashboard')
                else:
                    # If authentication fails, display an error message
                    messages.error(request, 'Invalid username or password.')
        else:
            # If it's a GET request (first time loading the page)
            form = LoginForm() # Create an empty form instance
        return render(request, 'dashboard/login.html', {'form': form}) # Render the login template

@login_required # Ensures only logged-in users can access this view
def user_logout(request):
        logout(request) # Log the user out
        messages.success(request, 'You have been logged out successfully.') # Display a success message
        return redirect('login') # Redirect to the login page

    # --- Placeholder Dashboard Views ---
    # These views will be fleshed out later. For now, they just render simple messages.

@login_required
@user_passes_test(is_professor, login_url='login') # Only professors can access, redirect to login if not
def professor_dashboard(request):
        # For now, just display a placeholder message
        return render(request, 'dashboard/professor_dashboard.html', {'message': 'Welcome to the Professor Dashboard!'})

@login_required
@user_passes_test(is_student, login_url='login') # Only students can access, redirect to login if not
def student_dashboard(request):
        # For now, just display a placeholder message
        return render(request, 'dashboard/student_dashboard.html', {'message': 'Welcome to the Student Dashboard!'})

    # This view will be for College Admins, to be built in Phase 4
@login_required
@user_passes_test(is_college_admin, login_url='login')
def college_admin_dashboard(request):
        return render(request, 'dashboard/college_admin_dashboard.html', {'message': 'Welcome to the College Admin Dashboard!'})

    