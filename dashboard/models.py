    # dashboard/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

    # 1. College Model: This is the foundation for multi-college support.
    # Every piece of data (users, subjects, results, etc.) will be linked to a specific college.
class College(models.Model):
        name = models.CharField(max_length=255, unique=True) # Unique name for each college
        province = models.CharField(max_length=100) # Province where the college is located
        address = models.TextField(blank=True, null=True) # Optional: Full address
        contact_email = models.EmailField(blank=True, null=True) # Optional: Contact email
        phone_number = models.CharField(max_length=20, blank=True, null=True) # Optional: Phone number

        # How a College object will be displayed (e.g., in Django Admin)
        def __str__(self):
            return self.name

    # 2. Custom User Model: Extends Django's default User model.
    # We add a 'user_type' to define roles and link each user to a 'College'.
class User(AbstractUser):
        USER_TYPE_CHOICES = (
            ("super_admin", "Super Admin"),
            ("college_admin", "College Admin"),
            ("professor", "Professor"),
            ("student", "Student"),
        )
        user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="student")
        # ForeignKey to College:
        # - on_delete=models.CASCADE: If a college is deleted, its users are also deleted.
        # - null=True, blank=True: Allows users (like a 'super_admin') to exist without being tied to a specific college.
        # - related_name='users': Allows us to easily get all users for a college (e.g., `my_college.users.all()`).
        college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True, related_name='users')

        def __str__(self):
            # Display full name if available, otherwise username
            return self.get_full_name() or self.username

    # 3. Professor Model: Stores extra details for professors.
    # OneToOneField means each Professor record is linked to exactly one User record, and vice-versa.
class Professor(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        department = models.CharField(max_length=100) # e.g., "Computer Science", "Mathematics"
        # The college association for a professor is managed through their linked User object.

        def __str__(self):
            return self.user.get_full_name() or self.user.username

    # 4. Student Model: Stores extra details for students.
    # Similar to Professor, linked to User with a OneToOneField.
class Student(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        student_id = models.CharField(max_length=20, unique=True) # Unique ID for each student
        major = models.CharField(max_length=100) # e.g., "Software Engineering", "Physics"
        enrollment_year = models.IntegerField(null=True, blank=True) # Year student enrolled

        def __str__(self):
            return self.user.get_full_name() or self.user.username

    # 5. Subject Model: Represents academic courses.
    # Each subject is assigned to a professor and belongs to a specific college.
class Subject(models.Model):
        name = models.CharField(max_length=100)
        code = models.CharField(max_length=20, unique=True) # e.g., "CS101", "MATH202"
        professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_subjects')
        credits = models.IntegerField(default=3) # Number of credits for the subject
        # Link to College: Ensures subjects are tied to a specific institution.
        college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='subjects')

        def __str__(self):
            return f"{self.name} ({self.college.name})" # Show subject name and its college

    # 6. Result Model: Stores student results for a subject.
    # Linked to a student, a subject, and the college.
class Result(models.Model):
        student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
        subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
        marks = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 85.50
        grade = models.CharField(max_length=5) # e.g., "A+", "B-"
        date_recorded = models.DateTimeField(auto_now_add=True) # Automatically sets creation date
        # Link to College: Ensures results are tied to a specific institution.
        college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='results')

        class Meta:
            # unique_together ensures that a student can only have one result for a specific subject
            # within a specific college. This prevents duplicate result entries.
            unique_together = ('student', 'subject', 'college')

        def __str__(self):
            return f"{self.student.user.username} - {self.subject.name} ({self.college.name}): {self.grade}"

    # 7. Attendance Model: Records student attendance for a subject on a specific date.
    # Linked to a student, a subject, a date, and the college.
class Attendance(models.Model):
        student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
        subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
        date = models.DateField() # The date of the attendance record
        is_present = models.BooleanField(default=True) # True for present, False for absent
        # Link to College: Ensures attendance is tied to a specific institution.
        college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='attendance_records')

        class Meta:
            # unique_together ensures only one attendance record per student, per subject, per date, per college.
            unique_together = ('student', 'subject', 'date', 'college')

        def __str__(self):
            status = 'Present' if self.is_present else 'Absent'
            return f"{self.student.user.username} - {self.subject.name} on {self.date} ({self.college.name}): {status}"

    # 8. Notification Model: For sending messages to users.
    # Notifications can be sent to a specific user and are associated with a college.
class Notification(models.Model):
        recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
        title = models.CharField(max_length=200)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True) # Timestamp of creation
        is_read = models.BooleanField(default=False) # To track if the user has read it
        sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
        # Link to College: This notification is relevant to this college.
        # It can be null if it's a global notification from a super admin (e.g., system wide announcement).
        college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True, related_name='college_notifications')

        def __str__(self):
            college_name = self.college.name if self.college else "Global"
            return f"Notification for {self.recipient.username} ({college_name}): {self.title}"

    