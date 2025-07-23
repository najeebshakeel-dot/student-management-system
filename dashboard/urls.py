"""    # dashboard/urls.py

from django.urls import path
from . import views # Import views from the current app (dashboard)

urlpatterns = [
        # Authentication URLs
        path('login/', views.user_login, name='login'), # URL for the login page
        path('logout/', views.user_logout, name='logout'), # URL for logging out

        # Professor URLs (will add more here later)
        path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),

        # Student URLs (will add more here later)
        path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    ]
    """
# dashboard/urls.py

from django.urls import path
from . import views # Import views from the current app (dashboard)

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'), # URL for the login page
    path('logout/', views.user_logout, name='logout'), # URL for logging out

    # Professor URLs
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),

    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # College Admin URLs (THIS IS THE MISSING LINE)
    path('college_admin/dashboard/', views.college_admin_dashboard, name='college_admin_dashboard'),
]
