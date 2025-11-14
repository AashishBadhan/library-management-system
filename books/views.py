from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Book, BookIssue, Review, Reservation, Category, Notification
from api.serializers import (
    BookSerializer, BookIssueSerializer, ReviewSerializer,
    ReservationSerializer, CategorySerializer
)
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django_ratelimit.decorators import ratelimit

User = get_user_model()

# Rate Limit Error View
def ratelimit_error(request, exception):
    """Custom rate limit error page"""
    return render(request, 'ratelimit.html', status=429)

# API Permission Classes
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.role == 'admin'

# API ViewSets
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


# Template-based Views
@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    """Login page view with rate limiting"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.error(request, 'Too many login attempts. Please try again in a few minutes.')
            return render(request, 'login.html')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


@ratelimit(key='ip', rate='5/m', method='POST')
def register_view(request):
    """Registration page view with rate limiting"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.error(request, 'Too many registration attempts. Please try again in a few minutes.')
            return render(request, 'register.html')
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validation
        if not username or not email or not password1 or not password2:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                # Set default role as student
                user.role = 'student'
                user.save()
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register.html')


def logout_view(request):
    """Logout user"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Main dashboard view"""
    user = request.user
    
    # Get statistics
    total_books = Book.objects.count()
    books_issued = BookIssue.objects.filter(
        user=user,
        actual_return_date__isnull=True
    ).count()
    
    # Due soon (within 3 days)
    due_soon = BookIssue.objects.filter(
        user=user,
        actual_return_date__isnull=True,
        return_date__lte=timezone.now() + timedelta(days=3)
    ).count()
    
    # Recent activities
    recent_activities = BookIssue.objects.filter(user=user).order_by('-issue_date')[:5]
    
    # Recommended books (popular books not issued by user)
    issued_book_ids = BookIssue.objects.filter(user=user).values_list('book_id', flat=True)
    recommended_books = Book.objects.exclude(id__in=issued_book_ids).order_by('-id')[:6]
    
    # Books due soon with details
    due_books = BookIssue.objects.filter(
        user=user,
        actual_return_date__isnull=True,
        return_date__lte=timezone.now() + timedelta(days=7)
    ).select_related('book').order_by('return_date')
    
    context = {
        'total_books': total_books,
        'books_issued': books_issued,
        'due_soon': due_soon,
        'notifications': 0,  # Can be implemented later
        'recent_activities': recent_activities,
        'recommended_books': recommended_books,
        'due_books': due_books,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def book_detail_view(request, book_id: int):
    """Display book details or 'Book details not added' message"""
    try:
        book = Book.objects.get(id=book_id)
        # For now, show a simple message
        context = {
            'book': book,
            'message': 'Book details not added'
        }
        return render(request, 'book_detail.html', context)
    except Book.DoesNotExist:
        raise Http404("Book not found")


@login_required
def book_list_view(request):
    """Books listing with filters and search"""
    books = Book.objects.all()
    
    # Search
    search_query = request.GET.get('search', '') or request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        books = books.filter(category_id=category_id)
    
    # Availability filter
    availability = request.GET.get('availability', '')
    if availability == 'available':
        books = books.filter(available__gt=0)
    elif availability == 'unavailable':
        books = books.filter(available=0)
    
    # Sorting
    sort_by = request.GET.get('sort', 'title')
    if sort_by in ['title', 'author', 'created_at']:
        books = books.order_by(sort_by)
    elif sort_by in ['-title', '-author', '-created_at']:
        books = books.order_by(sort_by)
    elif sort_by in ['newest', '-created_at']:
        books = books.order_by('-created_at') if hasattr(Book, 'created_at') else books.order_by('-id')
    elif sort_by in ['oldest', 'created_at']:
        books = books.order_by('created_at') if hasattr(Book, 'created_at') else books.order_by('id')
    
    # Pagination
    paginator = Paginator(books, 12)  # 12 books per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'books': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_availability': availability,
        'selected_sort': sort_by,
        'total_books': books.count(),
    }
    
    return render(request, 'book_list.html', context)


@login_required
def my_books_view(request):
    """User's issued books"""
    user = request.user
    
    # Get all book issues for user
    book_issues = BookIssue.objects.filter(user=user).select_related('book').order_by('-issue_date')
    
    # Calculate statistics
    active_issues = book_issues.filter(actual_return_date__isnull=True)
    returned_books = book_issues.filter(actual_return_date__isnull=False).count()
    overdue_books = active_issues.filter(return_date__lt=timezone.now()).count()
    due_soon_count = active_issues.filter(return_date__gte=timezone.now(), return_date__lte=timezone.now() + timedelta(days=3)).count()
    total_fines = sum([(issue.fine_amount or 0) for issue in book_issues])
    
    # No need to add calculated fields - they're already @property methods in the model
    # The properties (days_remaining, is_overdue, calculated_fine) will be accessible directly
    
    context = {
        'book_issues': book_issues,
        'active_books': active_issues.count(),
        'returned_count': returned_books,
        'overdue_count': overdue_books,
        'due_soon_count': due_soon_count,
        'total_fine': total_fines,
    }
    
    return render(request, 'my_books.html', context)


@login_required
def issue_book_view(request, book_id: int):
    """Create an issue request for a book. Students create 'requested'; admins can auto-approve."""
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid method')

    book = get_object_or_404(Book, id=book_id)

    # Parse return date from POST (YYYY-MM-DD)
    return_date_str = request.POST.get('return_date')
    if not return_date_str:
        messages.error(request, 'Return date is required.')
        return redirect('book_list')
    try:
        # make timezone-aware end-of-day
        naive = datetime.strptime(return_date_str, '%Y-%m-%d')
        aware = timezone.make_aware(datetime(naive.year, naive.month, naive.day, 23, 59, 0))
    except Exception:
        messages.error(request, 'Invalid return date.')
        return redirect('book_list')

    status_value = 'active' if request.user.is_staff else 'requested'

    # If admin (or auto-approve), ensure availability
    if status_value in ['active', 'approved']:
        if book.available <= 0:
            messages.error(request, 'Book is not available.')
            return redirect('book_list')

    issue = BookIssue.objects.create(
        book=book,
        user=request.user,
        return_date=aware,
        status=status_value,
    )

    # Decrement availability when immediately activated
    if status_value in ['active', 'approved']:
        book.available = max(0, book.available - 1)
        book.save()

    if status_value == 'requested':
        messages.success(request, f'Request submitted for "{book.title}". Awaiting approval.')
    else:
        messages.success(request, f'Book "{book.title}" issued successfully!')
    return redirect('my_books')


@login_required
def renew_book_view(request, issue_id: int):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=400)
    issue = get_object_or_404(BookIssue, id=issue_id, user=request.user)
    if issue.actual_return_date:
        return JsonResponse({'success': False, 'message': 'Already returned'}, status=400)
    if not issue.return_date:
        return JsonResponse({'success': False, 'message': 'No return date set'}, status=400)
    # extend by 14 days
    issue.return_date = issue.return_date + timedelta(days=14)
    issue.save()
    return JsonResponse({'success': True})


@login_required
def return_book_view(request, issue_id: int):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=400)
    issue = get_object_or_404(BookIssue, id=issue_id, user=request.user)
    if issue.actual_return_date:
        return JsonResponse({'success': False, 'message': 'Already returned'}, status=400)

    # finalize and increment availability
    issue.finalize_return()
    book = issue.book
    book.available = book.available + 1
    book.save()
    return JsonResponse({'success': True, 'fine': float(issue.fine_amount)})


@login_required
def pay_fine_view(request):
    """Simple fine settlement stub: mark user's overdue payments as paid."""
    # This can be replaced by integration with Razorpay/Stripe
    if request.method == 'POST':
        qs = BookIssue.objects.filter(user=request.user, payment_status__in=['pending', 'overdue'])
        updated = 0
        for issue in qs:
            if issue.fine_amount and issue.fine_amount > 0:
                issue.payment_status = 'paid'
                issue.save()
                updated += 1
        messages.success(request, f'Fine payment recorded for {updated} item(s).')
        return redirect('my_books')
    # GET: show a minimal confirmation page or redirect for now
    messages.info(request, 'No payment gateway configured. Marking as paid for demo. Click confirm to proceed.')
    return render(request, 'pay_fine.html', {})


@login_required
def approve_issue_view(request, issue_id: int):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    issue = get_object_or_404(BookIssue, id=issue_id)
    if issue.status not in ['requested', 'rejected']:
        messages.info(request, 'Issue not in a state to approve.')
        return redirect('admin_panel')
    book = issue.book
    if book.available <= 0:
        messages.error(request, 'Book not available to approve.')
        return redirect('admin_panel')
    issue.status = 'active'
    book.available -= 1
    book.save()
    issue.save()
    
    # Create notification for user
    Notification.create_notification(
        user=issue.user,
        notification_type='issue_approved',
        title=f'Book Issue Approved: {book.title}',
        message=f'Your request for "{book.title}" has been approved. Return by {issue.return_date.strftime("%B %d, %Y") if issue.return_date else "N/A"}.',
        link='/my-books/'
    )
    
    # Send email
    try:
        return_date_str = issue.return_date.strftime("%B %d, %Y") if issue.return_date else "soon"
        send_mail(
            f'Book Issue Approved: {book.title}',
            f'Hello {issue.user.username},\n\nYour request for "{book.title}" has been approved.\n\nPlease return it by {return_date_str}.\n\nThank you,\nLibrary Management',
            settings.EMAIL_HOST_USER,
            [issue.user.email],
            fail_silently=True
        )
    except:
        pass
    
    messages.success(request, 'Issue approved.')
    return redirect('admin_panel')


@login_required
def reject_issue_view(request, issue_id: int):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    issue = get_object_or_404(BookIssue, id=issue_id)
    if issue.status != 'requested':
        messages.info(request, 'Only requested issues can be rejected.')
        return redirect('admin_panel')
    issue.status = 'rejected'
    issue.save()
    
    # Create notification for user
    Notification.create_notification(
        user=issue.user,
        notification_type='issue_rejected',
        title=f'Book Issue Rejected: {issue.book.title}',
        message=f'Your request for "{issue.book.title}" has been rejected. Please contact the library for details.',
        link='/books/'
    )
    
    # Send email
    try:
        send_mail(
            f'Book Issue Rejected: {issue.book.title}',
            f'Hello {issue.user.username},\n\nYour request for "{issue.book.title}" has been rejected.\n\nPlease contact the library for more information.\n\nThank you,\nLibrary Management',
            settings.EMAIL_HOST_USER,
            [issue.user.email],
            fail_silently=True
        )
    except:
        pass
    
    messages.success(request, 'Issue rejected.')
    return redirect('admin_panel')


@login_required
def add_book_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category_id = request.POST.get('category')
        quantity = int(request.POST.get('quantity', 0) or 0)
        price = request.POST.get('price', '0')
        publication_date = request.POST.get('publication_date')
        description = request.POST.get('description', '')
        cover = request.FILES.get('cover_image')
        
        if not (title and author and isbn and category_id and publication_date):
            messages.error(request, 'Please fill all required fields.')
            return redirect('admin_panel')
        
        # Check for duplicate ISBN
        if Book.objects.filter(isbn=isbn).exists():
            messages.error(request, f'A book with ISBN "{isbn}" already exists. Please use a unique ISBN.')
            return redirect('admin_books')
        
        # Check for duplicate title with same author (case-insensitive)
        if Book.objects.filter(title__iexact=title, author__iexact=author).exists():
            messages.warning(request, f'A book titled "{title}" by {author} already exists. Are you sure you want to add a duplicate?')
            # Still allow but warn admin
        
        category = get_object_or_404(Category, id=category_id)
        try:
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                category=category,
                quantity=quantity,
                available=quantity,
                price=price,
                publication_date=publication_date,
                description=description,
                cover_image=cover
            )
            messages.success(request, f'Book "{book.title}" added successfully.')
            return redirect('admin_books')
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')
            return redirect('admin_books')
    return HttpResponseBadRequest('Invalid method')


@login_required
def add_category_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if not name:
            messages.error(request, 'Category name required.')
            return redirect('admin_panel')
        Category.objects.create(name=name, description=description)
        messages.success(request, 'Category added.')
        return redirect('admin_panel')
    return HttpResponseBadRequest('Invalid method')


@login_required
def admin_panel_view(request):
    """Admin panel - only accessible to staff"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin panel.')
        return redirect('dashboard')
    
    # Get all data for admin
    books = Book.objects.all().select_related('category')
    categories = Category.objects.all()
    users = User.objects.all()
    book_issues = BookIssue.objects.all().select_related('user', 'book').order_by('-issue_date')
    
    # Statistics
    total_books = books.count()
    total_users = users.count()
    total_issued = book_issues.filter(actual_return_date__isnull=True).count()
    total_categories = categories.count()
    
    context = {
        'books': books,
        'categories': categories,
        'users': users,
        'book_issues': book_issues,
        'total_books': total_books,
        'total_users': total_users,
        'total_issued': total_issued,
        'total_categories': total_categories,
    }
    
    return render(request, 'admin_panel.html', context)


# =========================
# Admin separate pages
# =========================
@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('dashboard')
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_issued = BookIssue.objects.filter(actual_return_date__isnull=True).count()
    overdue = BookIssue.objects.filter(actual_return_date__isnull=True, return_date__lt=timezone.now()).count()
    recent_issues = BookIssue.objects.select_related('book','user').order_by('-issue_date')[:10]
    pending_requests = BookIssue.objects.filter(status='requested').select_related('book', 'user').order_by('-issue_date')
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_issued': total_issued,
        'overdue_count': overdue,
        'recent_issues': recent_issues,
        'pending_requests': pending_requests,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_books_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    books = Book.objects.all().select_related('category').order_by('-id')
    categories = Category.objects.all()
    return render(request, 'admin/books.html', {'books': books, 'categories': categories})


@login_required
def edit_book_view(request, book_id):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        new_isbn = request.POST.get('isbn', book.isbn)
        
        # Check for duplicate ISBN (excluding current book)
        if new_isbn != book.isbn and Book.objects.filter(isbn=new_isbn).exists():
            messages.error(request, f'A book with ISBN "{new_isbn}" already exists. Please use a unique ISBN.')
            return redirect('admin_books')
        
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.isbn = new_isbn
        category_id = request.POST.get('category')
        if category_id:
            book.category = get_object_or_404(Category, id=category_id)
        book.quantity = int(request.POST.get('quantity', book.quantity) or book.quantity)
        book.available = int(request.POST.get('available', book.available) or book.available)
        book.price = request.POST.get('price', book.price)
        book.publication_date = request.POST.get('publication_date', book.publication_date)
        book.description = request.POST.get('description', book.description)
        if 'cover_image' in request.FILES:
            book.cover_image = request.FILES['cover_image']
        
        try:
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating book: {str(e)}')
        
        return redirect('admin_books')
    return redirect('admin_books')


@login_required
def delete_book_view(request, book_id):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully.')
        return redirect('admin_books')
    return redirect('admin_books')


@login_required
def admin_users_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})


@login_required
def edit_user_view(request, user_id):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        role = request.POST.get('role')
        if role:
            user.role = role
        is_active = request.POST.get('is_active') == 'on'
        user.is_active = is_active
        user.save()
        messages.success(request, f'User "{user.username}" updated successfully.')
        return redirect('admin_users')
    return redirect('admin_users')


@login_required
def admin_categories_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    categories = Category.objects.all().order_by('name')
    return render(request, 'admin/categories.html', {'categories': categories})


@login_required
def edit_category_view(request, category_id):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', category.description)
        category.save()
        messages.success(request, f'Category "{category.name}" updated successfully.')
        return redirect('admin_categories')
    return redirect('admin_categories')


@login_required
def delete_category_view(request, category_id):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted successfully.')
        return redirect('admin_categories')
    return redirect('admin_categories')


@login_required
def admin_fines_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    overdue_issues = BookIssue.objects.filter(actual_return_date__isnull=True, return_date__lt=timezone.now()).select_related('book','user')
    total_overdue = overdue_issues.count()
    total_amount = sum([(i.calculated_fine or 0) for i in overdue_issues])
    return render(request, 'admin/fines.html', {'overdue_issues': overdue_issues, 'total_overdue': total_overdue, 'total_amount': total_amount})


@login_required
def admin_reports_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    from django.db.models import Count, Sum, Q
    from datetime import datetime, timedelta
    import json
    
    # Date range filters (default: last 12 months)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    
    # Get date range from request if provided
    if request.GET.get('start_date'):
        try:
            start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
        except ValueError:
            pass
    if request.GET.get('end_date'):
        try:
            end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Key statistics
    total_books = Book.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    active_issues = BookIssue.objects.filter(status__in=['approved', 'active'], actual_return_date__isnull=True).count()
    
    # Calculate total fines from overdue books
    overdue_issues = BookIssue.objects.filter(actual_return_date__isnull=True, return_date__lt=timezone.now())
    total_fines = sum([(issue.calculated_fine or 0) for issue in overdue_issues])
    unpaid_fines = total_fines  # For now, consider all overdue fines as unpaid
    
    # Monthly issues - simplified approach without TruncMonth
    monthly_issues = []
    issues_labels = []
    issues_data = []
    
    # Get last 12 months data
    for i in range(11, -1, -1):
        month_date = end_date - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        if i == 0:
            month_end = end_date
        else:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        
        count = BookIssue.objects.filter(
            issue_date__gte=month_start,
            issue_date__lte=month_end
        ).count()
        
        issues_labels.append(month_start.strftime('%b %Y'))
        issues_data.append(count)
    
    # Monthly fines - simplified
    fines_labels = issues_labels.copy()
    fines_data = []
    
    for i in range(11, -1, -1):
        month_date = end_date - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        if i == 0:
            month_end = end_date
        else:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        
        month_issues = BookIssue.objects.filter(
            issue_date__gte=month_start,
            issue_date__lte=month_end,
            return_date__lt=timezone.now()
        )
        
        month_fine = sum([(issue.calculated_fine or 0) for issue in month_issues])
        fines_data.append(float(month_fine))
    
    # Book category distribution
    category_distribution = Book.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    category_labels = [item['category__name'] or 'Uncategorized' for item in category_distribution]
    category_data = [item['count'] for item in category_distribution]
    
    # Top borrowed books
    top_books = Book.objects.annotate(
        borrow_count=Count('bookissue')
    ).order_by('-borrow_count')[:10]
    
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'active_issues': active_issues,
        'total_fines': total_fines,
        'unpaid_fines': unpaid_fines,
        'start_date': start_date,
        'end_date': end_date,
        'issues_labels': json.dumps(issues_labels),
        'issues_data': json.dumps(issues_data),
        'fines_labels': json.dumps(fines_labels),
        'fines_data': json.dumps(fines_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'top_books': top_books,
    }
    
    return render(request, 'admin/reports.html', context)


# CSV Exports
import csv
from django.http import HttpResponse

@login_required
def export_books_csv(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=books.csv'
    writer = csv.writer(response)
    writer.writerow(['ID','Title','Author','ISBN','Category','Quantity','Available','Price','PublicationDate'])
    for b in Book.objects.select_related('category').all():
        writer.writerow([b.id, b.title, b.author, b.isbn, b.category.name if b.category else '', b.quantity, b.available, b.price, b.publication_date])
    return response


@login_required
def export_issues_csv(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=issues.csv'
    writer = csv.writer(response)
    writer.writerow(['ID','User','Book','IssueDate','ReturnDate','ReturnedAt','Fine','PaymentStatus','Status'])
    for i in BookIssue.objects.select_related('book','user').all():
        writer.writerow([i.id, i.user.username, i.book.title, i.issue_date, i.return_date, i.actual_return_date, i.fine_amount, i.payment_status, i.status])
    return response


# Admin user actions
@login_required
def toggle_user_status_view(request, user_id: int):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    u = get_object_or_404(User, id=user_id)
    u.is_active = not u.is_active
    u.save()
    messages.success(request, f'User {u.username} is now {"active" if u.is_active else "inactive"}.')
    return redirect('admin_users')


# Notification views
from django.http import JsonResponse

@login_required
def mark_all_read_view(request):
    """Mark all notifications as read for the current user."""
    if request.method == 'POST':
        Notification.mark_all_read(request.user)
        return JsonResponse({'status': 'success', 'message': 'All notifications marked as read'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def notifications_list_view(request):
    """Display all notifications for the current user."""
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications.html', {
        'notifications': notifications
    })


# PDF Export views
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

@login_required
def export_books_pdf(request):
    """Export all books as PDF report."""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    # Create buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#14b8a6'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Library Management System", title_style))
    elements.append(Paragraph("Books Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Table data
    books = Book.objects.select_related('category').all()
    data = [['ID', 'Title', 'Author', 'ISBN', 'Category', 'Qty', 'Available', 'Price']]
    
    for book in books:
        data.append([
            str(book.id),
            book.title[:30],  # Truncate long titles
            book.author[:20],
            book.isbn,
            book.category.name if book.category else 'N/A',
            str(book.quantity),
            str(book.available),
            f'${book.price}'
        ])
    
    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14b8a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Total Books: {books.count()}", styles['Normal']))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=books_report_{datetime.now().strftime("%Y%m%d")}.pdf'
    return response


@login_required
def export_issues_pdf(request):
    """Export all book issues as PDF report."""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    # Create buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=0.5*inch, rightMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#14b8a6'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Library Management System", title_style))
    elements.append(Paragraph("Book Issues Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Table data
    issues = BookIssue.objects.select_related('book', 'user').all()
    data = [['ID', 'User', 'Book', 'Issue Date', 'Return Date', 'Status', 'Fine']]
    
    for issue in issues:
        data.append([
            str(issue.id),
            issue.user.username[:15],
            issue.book.title[:25],
            issue.issue_date.strftime('%Y-%m-%d'),
            issue.return_date.strftime('%Y-%m-%d'),
            issue.status,
            f'${issue.fine_amount}'
        ])
    
    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14b8a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Statistics
    total_fines = BookIssue.objects.aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    unpaid_fines = BookIssue.objects.filter(payment_status='unpaid').aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    
    stats_text = f"""
    Total Issues: {issues.count()}<br/>
    Total Fines: ${total_fines:.2f}<br/>
    Unpaid Fines: ${unpaid_fines:.2f}<br/>
    Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """
    elements.append(Paragraph(stats_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=issues_report_{datetime.now().strftime("%Y%m%d")}.pdf'
    return response


@login_required
def export_fines_pdf(request):
    """Export fines report as PDF."""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    # Create buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#14b8a6'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Library Management System", title_style))
    elements.append(Paragraph("Fines Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Table data - only issues with fines
    issues = BookIssue.objects.filter(fine_amount__gt=0).select_related('book', 'user')
    data = [['ID', 'User', 'Book', 'Fine Amount', 'Payment Status', 'Return Date']]
    
    for issue in issues:
        data.append([
            str(issue.id),
            issue.user.username[:20],
            issue.book.title[:30],
            f'${issue.fine_amount}',
            issue.payment_status,
            issue.return_date.strftime('%Y-%m-%d')
        ])
    
    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Statistics
    total_fines = issues.aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    paid_fines = issues.filter(payment_status='paid').aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    unpaid_fines = issues.filter(payment_status='unpaid').aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    
    stats_text = f"""
    Total Fines: ${total_fines:.2f}<br/>
    Paid Fines: ${paid_fines:.2f}<br/>
    Unpaid Fines: ${unpaid_fines:.2f}<br/>
    Total Users with Fines: {issues.values('user').distinct().count()}<br/>
    Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """
    elements.append(Paragraph(stats_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=fines_report_{datetime.now().strftime("%Y%m%d")}.pdf'
    return response
