from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    available = models.IntegerField(validators=[MinValueValidator(0)])
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BookIssue(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),  # Actively issued
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username}"

    @property
    def days_remaining(self):
        if self.actual_return_date or not self.return_date:
            return None
        delta = (self.return_date.date() - timezone.now().date())
        return delta.days

    @property
    def is_overdue(self):
        if self.actual_return_date or not self.return_date:
            return False
        return self.return_date < timezone.now()

    @property
    def calculated_fine(self):
        """Dynamic fine (₹5 per overdue day) without persisting until return."""
        if not self.is_overdue or not self.return_date:
            return 0
        days = abs((timezone.now() - self.return_date).days)
        return days * 5

    def finalize_return(self):
        """Mark book as returned, compute and persist fine, update status & availability."""
        if not self.actual_return_date:
            self.actual_return_date = timezone.now()
        # Check for None before comparison
        if self.return_date and self.actual_return_date > self.return_date:
            overdue_days = (self.actual_return_date - self.return_date).days
            self.fine_amount = overdue_days * 5  # Persist fine using current rate
            if overdue_days > 0:
                self.payment_status = 'overdue'
        self.status = 'returned'
        self.save()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('book', 'user')
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username} - {self.rating}"

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled')
    ])
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username}"


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
