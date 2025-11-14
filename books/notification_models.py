from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Notification(models.Model):
    """
    Notification model for user alerts (book issued, due soon, overdue, etc.)
    """
    NOTIFICATION_TYPES = [
        ('issue_approved', 'Issue Approved'),
        ('issue_rejected', 'Issue Rejected'),
        ('due_soon', 'Due Soon'),
        ('overdue', 'Overdue'),
        ('returned', 'Book Returned'),
        ('fine_added', 'Fine Added'),
        ('fine_paid', 'Fine Paid'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)  # Optional link to related page
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @classmethod
    def create_notification(cls, user, notification_type, title, message, link=None):
        """Helper method to create notifications"""
        return cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link
        )
    
    @classmethod
    def mark_all_read(cls, user):
        """Mark all notifications as read for a user"""
        cls.objects.filter(user=user, is_read=False).update(is_read=True)
