"""
Quick URL Testing Script
Tests all major URLs and reports which ones have errors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Create test client
client = Client()

# Test URLs
urls_to_test = {
    'Public URLs': [
        ('Login Page', '/'),
        ('Register Page', '/register/'),
        ('Login Direct', '/login/'),
    ],
    'Student URLs (need login)': [
        ('Dashboard', '/dashboard/'),
        ('Browse Books', '/books/'),
        ('My Books', '/my-books/'),
        ('Profile', '/profile/'),
        ('Notifications', '/notifications/'),
    ],
    'Admin URLs (need admin login)': [
        ('Admin Dashboard', '/admin/dashboard/'),
        ('Manage Books', '/admin/books/'),
        ('Manage Users', '/admin/users/'),
        ('Manage Categories', '/admin/categories/'),
        ('Fines', '/admin/fines/'),
        ('Reports', '/admin/reports/'),
    ],
    'Export URLs (need admin login)': [
        ('Export Books CSV', '/admin/export/books.csv'),
        ('Export Issues CSV', '/admin/export/issues.csv'),
        ('Export Books PDF', '/admin/export/books.pdf'),
        ('Export Issues PDF', '/admin/export/issues.pdf'),
        ('Export Fines PDF', '/admin/export/fines.pdf'),
    ]
}

print("=" * 80)
print("🧪 TESTING ALL URLs")
print("=" * 80)

# Test without login
print("\n📋 Testing Public URLs (No Login)...")
print("-" * 80)
for name, url in urls_to_test['Public URLs']:
    try:
        response = client.get(url)
        status = response.status_code
        if status == 200:
            print(f"✅ {name:30} {url:40} [{status}]")
        elif status == 302:
            print(f"🔄 {name:30} {url:40} [Redirect to: {response.url}]")
        else:
            print(f"⚠️  {name:30} {url:40} [{status}]")
    except Exception as e:
        print(f"❌ {name:30} {url:40} [ERROR: {str(e)[:50]}]")

# Login as student
print("\n📋 Testing Student URLs (Logged in as Student)...")
print("-" * 80)
try:
    # Get or create student user
    student, created = User.objects.get_or_create(
        username='test_student',
        defaults={
            'email': 'student@test.com',
            'role': 'student',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        student.set_password('testpass123')
        student.save()
    
    # Login
    client.login(username='test_student', password='testpass123')
    
    for name, url in urls_to_test['Student URLs (need login)']:
        try:
            response = client.get(url)
            status = response.status_code
            if status == 200:
                print(f"✅ {name:30} {url:40} [{status}]")
            elif status == 302:
                print(f"🔄 {name:30} {url:40} [Redirect]")
            elif status == 403:
                print(f"🔒 {name:30} {url:40} [Permission Denied]")
            else:
                print(f"⚠️  {name:30} {url:40} [{status}]")
        except Exception as e:
            print(f"❌ {name:30} {url:40} [ERROR: {str(e)[:50]}]")
    
    # Logout
    client.logout()
except Exception as e:
    print(f"❌ Failed to test student URLs: {e}")

# Login as admin
print("\n📋 Testing Admin URLs (Logged in as Admin)...")
print("-" * 80)
try:
    # Get or create admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@test.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
    
    # Login as admin
    client.login(username='admin', password='admin123')
    
    all_admin_urls = urls_to_test['Admin URLs (need admin login)'] + urls_to_test['Export URLs (need admin login)']
    
    for name, url in all_admin_urls:
        try:
            response = client.get(url)
            status = response.status_code
            if status == 200:
                print(f"✅ {name:30} {url:40} [{status}]")
            elif status == 302:
                print(f"🔄 {name:30} {url:40} [Redirect]")
            else:
                print(f"⚠️  {name:30} {url:40} [{status}]")
        except Exception as e:
            print(f"❌ {name:30} {url:40} [ERROR: {str(e)[:50]}]")
    
    client.logout()
except Exception as e:
    print(f"❌ Failed to test admin URLs: {e}")

print("\n" + "=" * 80)
print("✅ URL Testing Complete!")
print("=" * 80)
print("\n📝 Legend:")
print("  ✅ = Working perfectly (200)")
print("  🔄 = Redirect (302)")
print("  🔒 = Permission denied (403)")
print("  ⚠️  = Other status code")
print("  ❌ = Error/Exception")
print()
