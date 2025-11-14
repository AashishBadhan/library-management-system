from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views, auth_views
from books.views import (
    login_view, register_view, logout_view, dashboard_view,
    book_list_view, book_detail_view, my_books_view, admin_panel_view,
    issue_book_view, renew_book_view, return_book_view,
    pay_fine_view, approve_issue_view, reject_issue_view,
    add_book_view, add_category_view,
    admin_dashboard_view, admin_books_view, admin_users_view,
    admin_categories_view, admin_fines_view, admin_reports_view,
    export_books_csv, export_issues_csv, toggle_user_status_view,
    edit_book_view, delete_book_view, edit_category_view, delete_category_view,
    edit_user_view,
    mark_all_read_view, notifications_list_view,
    export_books_pdf, export_issues_pdf, export_fines_pdf
)
from users.views import profile_view
from users.password_reset import forgot_password_view, reset_password_view
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'bookissues', views.BookIssueViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    # Template-based views (New Modern UI)
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
    path('notifications/mark-all-read/', mark_all_read_view, name='mark_all_read'),
    path('notifications/', notifications_list_view, name='notifications_list'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('books/', book_list_view, name='book_list'),
    path('books/<int:book_id>/', book_detail_view, name='book_detail'),
    path('search/', book_list_view, name='search'),
    path('my-books/', my_books_view, name='my_books'),
    path('profile/', profile_view, name='user_profile'),
    path('admin-panel/', admin_panel_view, name='admin_panel'),  # legacy combined panel
    
    # Custom Admin Pages (MUST be before Django's admin to avoid catch-all conflict)
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin/books/', admin_books_view, name='admin_books'),
    path('admin/users/', admin_users_view, name='admin_users'),
    path('admin/categories/', admin_categories_view, name='admin_categories'),
    path('admin/fines/', admin_fines_view, name='admin_fines'),
    path('admin/reports/', admin_reports_view, name='admin_reports'),
    path('admin/books/add/', add_book_view, name='add_book'),
    path('admin/books/<int:book_id>/edit/', edit_book_view, name='edit_book'),
    path('admin/books/<int:book_id>/delete/', delete_book_view, name='delete_book'),
    path('admin/categories/add/', add_category_view, name='add_category'),
    path('admin/categories/<int:category_id>/edit/', edit_category_view, name='edit_category'),
    path('admin/categories/<int:category_id>/delete/', delete_category_view, name='delete_category'),
    path('admin/users/<int:user_id>/edit/', edit_user_view, name='edit_user'),
    path('admin/users/toggle/<int:user_id>/', toggle_user_status_view, name='toggle_user_status'),
    path('admin/export/books.csv', export_books_csv, name='export_books_csv'),
    path('admin/export/issues.csv', export_issues_csv, name='export_issues_csv'),
    path('admin/export/books.pdf', export_books_pdf, name='export_books_pdf'),
    path('admin/export/issues.pdf', export_issues_pdf, name='export_issues_pdf'),
    path('admin/export/fines.pdf', export_fines_pdf, name='export_fines_pdf'),
    
    # Django Built-in Admin (MUST be after custom admin URLs)
    path('admin/', admin.site.urls),
    
    # Borrowing & fines
    path('books/<int:book_id>/request-issue/', issue_book_view, name='issue_book'),
    path('books/renew/<int:issue_id>/', renew_book_view, name='renew_book'),
    path('books/return/<int:issue_id>/', return_book_view, name='return_book'),
    # Legacy alias used by existing JS
    path('books/<int:book_id>/issue/', issue_book_view, name='issue_book_legacy'),
    path('pay-fine/', pay_fine_view, name='pay_fine'),
    # Admin issue workflow
    path('issues/<int:issue_id>/approve/', approve_issue_view, name='approve_issue'),
    path('issues/<int:issue_id>/reject/', reject_issue_view, name='reject_issue'),
    
    # API endpoints (for Next.js frontend)
    path('api/auth/register/', auth_views.register, name='api_register'),
    path('api/auth/login/', auth_views.login, name='api_login'),
    path('api/auth/profile/', auth_views.get_user_profile, name='profile'),
    path('api/auth/my-books/', auth_views.get_my_books, name='api_my_books'),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
