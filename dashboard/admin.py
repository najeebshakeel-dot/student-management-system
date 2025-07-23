"""    # dashboard/admin.py

from django.contrib import admin
from .models import College, User, Professor, Student, Subject, Result, Attendance, Notification

    # Register your models here so they appear in the Django admin interface.
    # This allows you to easily add, edit, and delete records for these models.
admin.site.register(College)
admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Result)
admin.site.register(Attendance)
admin.site.register(Notification)
    """
# dashboard/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Import Django's UserAdmin
from .models import College, User, Professor, Student, Subject, Result, Attendance, Notification
from .forms import CustomUserChangeForm, CustomUserCreationForm # Import your custom admin forms

# Register your models here so they appear in the Django admin interface.
admin.site.register(College) # Keep this

# Custom Admin class for your User model
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm # Form for editing existing users
    add_form = CustomUserCreationForm # Form for adding new users

    # Fields to display in the user list in admin
    list_display = ('username', 'email', 'user_type', 'college', 'is_staff', 'is_active',)
    # Fields to use for searching users
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    # Filters to apply to the user list
    list_filter = ('user_type', 'college', 'is_staff', 'is_active',)

    # Fieldsets for organizing fields on the user edit page
    # This adds 'user_type' and 'college' to the standard user fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'college',)}),
    )
    # Fieldsets for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'college',)}),
    )

# Unregister the default User model if it was registered, then register your custom UserAdmin
# This ensures your custom admin class takes precedence and avoids conflicts.
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass # User not yet registered, no need to unregister

admin.site.register(User, CustomUserAdmin) # Register your User model with your custom admin class

# Keep other model registrations as they were
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Result)
admin.site.register(Attendance)
admin.site.register(Notification)
