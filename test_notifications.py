"""
Test Notification System
This script modifies book issue dates to test notification system
"""
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from books.models import BookIssue, Notification
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

def clear_old_notifications():
    """Clear existing notifications for fresh test"""
    count = Notification.objects.all().count()
    if count > 0:
        Notification.objects.all().delete()
        print(f"✓ Cleared {count} old notifications")
    else:
        print("✓ No old notifications to clear")

def setup_test_scenarios():
    """Create different test scenarios with book issues"""
    print("\n" + "="*60)
    print("SETTING UP TEST SCENARIOS")
    print("="*60)
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@library.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"✓ Created test user: {user.username}")
    else:
        print(f"✓ Using existing user: {user.username}")
    
    # Get active book issues
    active_issues = BookIssue.objects.filter(
        actual_return_date__isnull=True,
        status__in=['approved', 'active']
    ).select_related('book', 'user')
    
    if active_issues.count() == 0:
        print("❌ No active book issues found!")
        print("   Please issue some books first from the web interface")
        return False
    
    print(f"\n✓ Found {active_issues.count()} active book issues")
    print("\nModifying dates for testing:\n")
    
    count = 0
    scenarios = [
        (2, "Due in 2 days - Should trigger early reminder"),
        (1, "Due tomorrow - Should trigger urgent reminder"),
        (0, "Due today - Should trigger final notice"),
        (-1, "1 day overdue - Should trigger overdue notice with ₹5 fine"),
        (-7, "7 days overdue - Should trigger overdue notice with ₹35 fine"),
    ]
    
    for issue in active_issues[:5]:  # Use first 5 issues
        if count >= len(scenarios):
            break
        
        days, description = scenarios[count]
        new_return_date = timezone.now() + timedelta(days=days)
        
        old_date = issue.return_date
        
        # Ensure issue_date is set
        if not issue.issue_date:
            issue.issue_date = timezone.now() - timedelta(days=7)  # Set to 7 days ago
        
        issue.return_date = new_return_date
        issue.save()
        
        print(f"  {count+1}. Book: {issue.book.title[:40]}")
        print(f"     User: {issue.user.username}")
        print(f"     Old date: {old_date.strftime('%Y-%m-%d %H:%M') if old_date else 'Not set'}")
        print(f"     New date: {new_return_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"     Scenario: {description}")
        print()
        
        count += 1
    
    print(f"✓ Modified {count} book issues for testing")
    return True

def run_notification_system():
    """Run the notification management command"""
    print("\n" + "="*60)
    print("RUNNING NOTIFICATION SYSTEM")
    print("="*60 + "\n")
    
    from django.core.management import call_command
    
    try:
        call_command('send_notifications')
        return True
    except Exception as e:
        print(f"❌ Error running notifications: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def display_results():
    """Display notifications created"""
    print("\n" + "="*60)
    print("NOTIFICATION RESULTS")
    print("="*60 + "\n")
    
    notifications = Notification.objects.all().order_by('-created_at')
    
    if notifications.count() == 0:
        print("❌ No notifications were created!")
        print("   Check if email settings are configured properly")
        return
    
    print(f"✓ Total notifications created: {notifications.count()}\n")
    
    # Group by type
    types = {}
    for notif in notifications:
        if notif.notification_type not in types:
            types[notif.notification_type] = []
        types[notif.notification_type].append(notif)
    
    # Display by type
    type_names = {
        'due_soon': '📅 DUE SOON',
        'overdue': '⛔ OVERDUE'
    }
    
    for notif_type, notif_list in types.items():
        print(f"\n{type_names.get(notif_type, notif_type.upper())} ({len(notif_list)} notifications):")
        print("-" * 60)
        
        for notif in notif_list:
            print(f"  User: {notif.user.username}")
            print(f"  Title: {notif.title}")
            print(f"  Message: {notif.message}")
            print(f"  Created: {notif.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

def check_email_config():
    """Check if email is configured"""
    from django.conf import settings
    
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION CHECK")
    print("="*60 + "\n")
    
    email_backend = getattr(settings, 'EMAIL_BACKEND', None)
    email_host = getattr(settings, 'EMAIL_HOST', None)
    email_host_user = getattr(settings, 'EMAIL_HOST_USER', None)
    
    if email_backend and 'console' in email_backend.lower():
        print("✓ Email Backend: Console (emails will print to terminal)")
    elif email_backend and 'smtp' in email_backend.lower():
        print(f"✓ Email Backend: SMTP")
        print(f"  Host: {email_host or 'Not configured'}")
        print(f"  User: {email_host_user or 'Not configured'}")
    else:
        print(f"⚠️  Email Backend: {email_backend or 'Not configured'}")
        print("   Emails may not be sent!")

def restore_dates():
    """Ask user if they want to restore original dates"""
    print("\n" + "="*60)
    print("DATE RESTORATION")
    print("="*60 + "\n")
    
    response = input("Do you want to restore original dates? (y/n): ").lower().strip()
    
    if response == 'y':
        # Reset all active issues to 14 days from now
        active_issues = BookIssue.objects.filter(
            actual_return_date__isnull=True,
            status__in=['approved', 'active']
        )
        
        new_date = timezone.now() + timedelta(days=14)
        count = active_issues.update(return_date=new_date)
        
        print(f"✓ Restored {count} book issues to 14 days from now")
        print(f"  New return date: {new_date.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("⚠️  Dates NOT restored - books will keep test dates!")
        print("   You can manually restore from admin panel if needed")

def main():
    """Main test function"""
    print("\n" + "="*70)
    print(" "*15 + "NOTIFICATION SYSTEM TEST")
    print("="*70)
    
    try:
        # Step 1: Check email config
        check_email_config()
        
        # Step 2: Clear old notifications
        clear_old_notifications()
        
        # Step 3: Setup test scenarios
        if not setup_test_scenarios():
            print("\n❌ Setup failed. Exiting...")
            return
        
        # Step 4: Run notification system
        if not run_notification_system():
            print("\n❌ Notification system failed. Check errors above.")
            return
        
        # Step 5: Display results
        display_results()
        
        # Step 6: Ask about date restoration
        restore_dates()
        
        print("\n" + "="*70)
        print(" "*20 + "TEST COMPLETED!")
        print("="*70)
        print("\n✓ Check your email inbox for notification emails")
        print("✓ Check web interface bell icon for in-app notifications")
        print("✓ Login to see notifications at: http://127.0.0.1:8000/notifications/")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
