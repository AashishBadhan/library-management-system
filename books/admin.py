from django.contrib import admin
from .models import Book, Category, BookIssue, Review, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'quantity', 'available', 'price']
    list_filter = ['category']
    search_fields = ['title', 'author', 'isbn']

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'issue_date', 'return_date', 'fine_amount', 'payment_status']
    list_filter = ['payment_status', 'issue_date']
    search_fields = ['book__title', 'user__username']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'reservation_date', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['book__title', 'user__username']
