import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create test user
if not User.objects.filter(username='test').exists():
    user = User.objects.create_user(
        username='test',
        email='test@test.com',
        password='test123'
    )
    print("✅ Test user created successfully!")
    print("Username: test")
    print("Password: test123")
else:
    print("ℹ️ Test user already exists")
    print("Username: test")
    print("Password: test123")
