"""  # dashboard/forms.py

from django import forms


    # This form will handle user login with username and password.
class LoginForm(forms.Form):
        # CharField for text input.
        # widget=forms.TextInput specifies it's a single-line text box.
        # attrs={'class': '...'} applies Tailwind CSS classes for styling.
        username = forms.CharField(
            max_length=150,
            widget=forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
        )
        # PasswordInput widget hides the input for security.
        password = forms.CharField(
            widget=forms.PasswordInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
        )
    

    # We will add more forms here later, like for results or attendance.
    """
# dashboard/forms.py

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm # Import these
from .models import User # Import your custom User model

# This form will handle user login with username and password.
class LoginForm(forms.Form):
    # CharField for text input.
    # widget=forms.TextInput specifies it's a single-line text box.
    # attrs={'class': '...'} applies Tailwind CSS classes for styling.
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )
    # PasswordInput widget hides the input for security.
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )

# Custom form for User model in Django Admin
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        # Ensure all fields are included, or specify which ones to show
        fields = '__all__' # Or a tuple of fields you want to display

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type', 'college',) # Specify fields for creation

# We will add more forms here later, like for results or attendance.
