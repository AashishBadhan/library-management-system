from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from books.models import Book, BookIssue, Review, Reservation, Category
from .serializers import (
    BookSerializer, BookIssueSerializer, ReviewSerializer,
    ReservationSerializer, CategorySerializer, UserSerializer
)
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.role == 'admin'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        book = self.get_object()
        user = request.user
        
        if book.available > 0:
            reservation = Reservation.objects.create(
                book=book,
                user=user,
                status='pending'
            )
            book.available -= 1
            book.save()
            
            # Send email notification
            send_mail(
                'Book Reservation Confirmation',
                f'Your reservation for {book.title} has been confirmed.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            return Response({'status': 'reservation created'})
        return Response(
            {'error': 'Book not available'},
            status=status.HTTP_400_BAD_REQUEST
        )

class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book_issue = self.get_object()
        book_issue.actual_return_date = timezone.now()
        
        # Calculate fine if overdue
        if book_issue.actual_return_date > book_issue.return_date:
            days_overdue = (book_issue.actual_return_date - book_issue.return_date).days
            book_issue.fine_amount = days_overdue * 1.0  # $1 per day
            book_issue.payment_status = 'overdue'
        
        book_issue.save()
        
        # Update book availability
        book = book_issue.book
        book.available += 1
        book.save()
        
        return Response({'status': 'book returned', 'fine_amount': book_issue.fine_amount})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == 'pending':
            reservation.status = 'cancelled'
            reservation.save()
            
            # Update book availability
            book = reservation.book
            book.available += 1
            book.save()
            
            return Response({'status': 'reservation cancelled'})
        return Response(
            {'error': 'Cannot cancel this reservation'},
            status=status.HTTP_400_BAD_REQUEST
        )
