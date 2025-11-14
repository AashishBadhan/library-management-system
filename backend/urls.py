"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from books.views import (
    BookViewSet, CategoryViewSet, BookIssueViewSet, ReviewViewSet, ReservationViewSet,
    login_view, register_view, logout_view, dashboard_view, book_list_view, my_books_view, admin_panel_view
)
from users.views import UserViewSet
from api.auth_views import register, login, get_user_profile, get_my_books

# Create router for API endpoints
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'book-issues', BookIssueViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Template-based views
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('books/', book_list_view, name='book_list'),
    path('my-books/', my_books_view, name='my_books'),
    path('admin-panel/', admin_panel_view, name='admin_panel'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', register, name='api_register'),
    path('api/auth/login/', login, name='api_login'),
    path('api/auth/profile/', get_user_profile, name='api_profile'),
    path('api/auth/my-books/', get_my_books, name='api_my_books'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
