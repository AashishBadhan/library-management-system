from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from books.models import BookIssue, Notification
from datetime import timedelta


class Command(BaseCommand):
    help = 'Send email notifications for due/overdue books'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking for due and overdue books...')
        
        # Find books due in 2 days
        two_days = timezone.now() + timedelta(days=2)
        due_in_two = BookIssue.objects.filter(
            actual_return_date__isnull=True,
            return_date__date=two_days.date(),
            status__in=['approved', 'active']
        ).select_related('book', 'user')
        
        for issue in due_in_two:
            # Create notification first (don't depend on email)
            Notification.create_notification(
                user=issue.user,
                notification_type='due_soon',
                title=f'Book Due in 2 Days: {issue.book.title}',
                message=f'Please return "{issue.book.title}" by {issue.return_date.strftime("%B %d, %Y")} to avoid fines.',
                link='/my-books/'
            )
            
            try:
                # Send email (fail silently if email fails)
                subject = f'Reminder: Book "{issue.book.title}" Due in 2 Days'
                message = f"""
Hello {issue.user.username},

This is a reminder that the book "{issue.book.title}" is due for return in 2 days ({issue.return_date.strftime('%B %d, %Y')}).

Please plan to return it on time to avoid late fees (₹5 per day).

Thank you,
Library Management System
"""
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [issue.user.email],
                    fail_silently=True
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Sent 2-day reminder to {issue.user.email}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Email failed for {issue.user.email}: {str(e)} (notification created)'))
        
        # Find books due in 1 day (tomorrow)
        tomorrow = timezone.now() + timedelta(days=1)
        due_tomorrow = BookIssue.objects.filter(
            actual_return_date__isnull=True,
            return_date__date=tomorrow.date(),
            status__in=['approved', 'active']
        ).select_related('book', 'user')
        
        for issue in due_tomorrow:
            # Create notification first
            Notification.create_notification(
                user=issue.user,
                notification_type='due_soon',
                title=f'⚠️ Due Tomorrow: {issue.book.title}',
                message=f'URGENT: Return "{issue.book.title}" by tomorrow ({issue.return_date.strftime("%B %d, %Y")}) to avoid ₹5/day fine.',
                link='/my-books/'
            )
            
            try:
                # Send email
                subject = f'⚠️ Urgent: Book "{issue.book.title}" Due Tomorrow'
                message = f"""
Hello {issue.user.username},

URGENT REMINDER: The book "{issue.book.title}" is due for return TOMORROW ({issue.return_date.strftime('%B %d, %Y')}).

Please return it on time to avoid late fees (₹5 per day starting the next day).

Thank you,
Library Management System
"""
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [issue.user.email],
                    fail_silently=True
                )
                self.stdout.write(self.style.WARNING(f'✓ Sent urgent 1-day reminder to {issue.user.email}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Email failed for {issue.user.email}: {str(e)} (notification created)'))
        
        # Find books due TODAY (last day)
        today = timezone.now().date()
        due_today = BookIssue.objects.filter(
            actual_return_date__isnull=True,
            return_date__date=today,
            status__in=['approved', 'active']
        ).select_related('book', 'user')
        
        for issue in due_today:
            # Create notification first
            Notification.create_notification(
                user=issue.user,
                notification_type='due_soon',
                title=f'🚨 DUE TODAY: {issue.book.title}',
                message=f'FINAL NOTICE: Return "{issue.book.title}" TODAY ({issue.return_date.strftime("%B %d, %Y")}) to avoid fines!',
                link='/my-books/'
            )
            
            try:
                # Send email
                subject = f'🚨 FINAL NOTICE: Book "{issue.book.title}" Due TODAY'
                message = f"""
Hello {issue.user.username},

FINAL NOTICE: The book "{issue.book.title}" is due for return TODAY ({issue.return_date.strftime('%B %d, %Y')}).

Please return it before the library closes today to avoid late fees (₹5 per day starting tomorrow).

Thank you,
Library Management System
"""
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [issue.user.email],
                    fail_silently=True
                )
                self.stdout.write(self.style.ERROR(f'✓ Sent FINAL notice to {issue.user.email}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Email failed for {issue.user.email}: {str(e)} (notification created)'))
        
        # Find overdue books
        overdue = BookIssue.objects.filter(
            actual_return_date__isnull=True,
            return_date__lt=timezone.now(),
            status__in=['approved', 'active']
        ).select_related('book', 'user')
        
        for issue in overdue:
            days_overdue = (timezone.now().date() - issue.return_date.date()).days
            fine = days_overdue * 5
            
            # Create notification first
            Notification.create_notification(
                user=issue.user,
                notification_type='overdue',
                title=f'⛔ OVERDUE: {issue.book.title}',
                message=f'{days_overdue} days overdue. Fine: ₹{fine}. Please return immediately to avoid additional charges!',
                link='/my-books/'
            )
            
            try:
                subject = f'⛔ OVERDUE NOTICE: Book "{issue.book.title}" - ₹{fine} Fine'
                message = f"""
Hello {issue.user.username},

The book "{issue.book.title}" is now {days_overdue} day(s) OVERDUE.

Current fine: ₹{fine} (₹5 per day)
Return due date was: {issue.return_date.strftime('%B %d, %Y')}

Please return the book IMMEDIATELY to avoid further charges.

Thank you,
Library Management System
"""
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [issue.user.email],
                    fail_silently=True
                )
                self.stdout.write(self.style.ERROR(f'✓ Sent overdue notice to {issue.user.email} (₹{fine})'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Email failed for {issue.user.email}: {str(e)} (notification created)'))
        
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  • 2 days before: {due_in_two.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  • 1 day before: {due_tomorrow.count()}'))
        self.stdout.write(self.style.ERROR(f'  • Due today: {due_today.count()}'))
        self.stdout.write(self.style.ERROR(f'  • Overdue: {overdue.count()}'))
