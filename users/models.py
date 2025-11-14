from django.contrib.auth.models import AbstractUser
from django.db import models

# CustomUser temporarily disabled to avoid conflicts with default User model
# Uncomment and configure AUTH_USER_MODEL = 'users.CustomUser' in settings.py for production

class CustomUser(AbstractUser):
	phone_number = models.CharField(max_length=15, blank=True)
	address = models.TextField(blank=True)
	role = models.CharField(
		max_length=20,
		choices=[
			('student', 'Student'),
			('librarian', 'Librarian'),
			('admin', 'Admin')
		],
		default='student'
	)
	profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

	def __str__(self):
		return self.username
