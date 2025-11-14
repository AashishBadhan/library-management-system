# Library Management System

A modern, feature-rich Library Management System built with Django and vanilla JavaScript, offering separate admin and user interfaces with professional-grade functionality.

## 🌟 Features

### User Features
- **Browse Books**: Filter and search through the book catalog with grid/list view toggle
- **Issue Books**: Request book loans with automated approval workflow
- **Manage Borrowed Books**: View active loans, due dates, overdue fines, and return status
- **Profile Management**: Update personal information and upload profile picture
- **Fine Settlement**: View and settle overdue fines (ready for payment gateway integration)
- **Responsive Design**: Teal-themed UI with glassmorphism effects and dark mode support

### Admin Features
- **Separated Admin Panel**: Dedicated dark-themed admin interface with sidebar navigation
- **Dashboard Analytics**: Overview statistics including total books, active issues, and overdue fines
- **Complete CRUD Operations**:
  - **Books**: Add, edit, delete books with cover images and category management
  - **Categories**: Manage book categories with inline editing
  - **Users**: Edit user details, roles, and toggle account status
- **Issue Management**: Approve/reject book requests, track returns, manage overdue items
- **Fine Administration**: Monitor overdue books and calculate fines automatically
- **Data Export**: CSV exports for books and issue records
- **Reports**: Overview of borrowing trends and library statistics

### Technical Features
- **Custom User Model**: Extended with phone, address, role, and profile picture fields
- **Role-Based Access Control**: Staff vs student permissions with decorator-based guards
- **RESTful API**: Django REST Framework endpoints for potential frontend integration
- **Email Notifications**: Infrastructure ready for issue/due/overdue alerts
- **Secure Authentication**: CSRF protection, login_required decorators, and password validation
- **Responsive Tables**: Sortable, filterable data tables with pagination support

## 🛠 Technology Stack

- **Backend**: Django 5.2.x, Django REST Framework
- **Database**: SQLite (dev), PostgreSQL-ready (production)
- **Frontend**: Django Templates, Vanilla JavaScript, CSS3
- **UI**: Custom teal theme with glassmorphism, Font Awesome icons, Inter font
- **Deployment**: Configured for Gunicorn, Whitenoise static files, AWS S3 media storage

## 📁 Project Structure

```
Web-Application/
├── library_management/        # Project settings and URLs
│   ├── settings.py           # Configuration with environment variable support
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI application
├── books/                     # Core library app
│   ├── models.py             # Book, BookIssue, Category, Review, Reservation
│   ├── views.py              # Template views and business logic
│   ├── templatetags/         # Custom template filters (e.g., abs)
│   └── migrations/
├── users/                     # User management app
│   ├── models.py             # CustomUser model
│   ├── views.py              # Profile view
│   └── migrations/
├── api/                       # REST API app
│   ├── views.py              # API ViewSets
│   ├── serializers.py        # DRF serializers
│   └── auth_views.py         # Authentication endpoints
├── templates/
│   ├── base.html             # User panel base layout
│   ├── layouts/
│   │   └── admin_base.html   # Admin panel base layout
│   ├── login.html            # Authentication page
│   ├── dashboard.html        # User dashboard
│   ├── book_list.html        # Browse books with filters
│   ├── my_books.html         # User's borrowed books
│   ├── profile.html          # User profile editor
│   └── admin/                # Admin templates
│       ├── dashboard.html
│       ├── books.html        # Book CRUD with modals
│       ├── users.html        # User management
│       ├── categories.html   # Category management
│       ├── fines.html        # Overdue tracking
│       └── reports.html      # Analytics stub
├── static/
│   ├── css/
│   │   ├── style-teal.css    # User theme
│   │   └── admin.css         # Admin dark theme
│   ├── js/
│   │   └── script.js         # Sidebar, dropdown, toasts
│   └── images/
├── media/                     # User-uploaded files (avatars, book covers)
├── manage.py
└── requirements.txt
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- pip
- Virtual environment tool (venv)
- Git (optional)

### Installation

1. **Clone or extract the project**
   ```bash
   cd "C:\Users\qq\Desktop\Libraray Management Project completed"
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   cd Web-Application
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional for dev)
   - Copy `.env.example` to `.env` (if provided)
   - Update `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` for email features
   - For production, set `DEBUG=False`, `ALLOWED_HOSTS`, `SECRET_KEY`

5. **Run migrations**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```powershell
   python manage.py createsuperuser --username admin --email admin@example.com
   # Enter password when prompted (demo: admin/admin)
   ```

7. **Collect static files**
   ```powershell
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```powershell
   python manage.py runserver
   ```

9. **Access the application**
   - User interface: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/dashboard/
   - Django admin: http://127.0.0.1:8000/admin/ (built-in)

### Sample Credentials
- **Admin**: `admin` / `admin` (or password set during createsuperuser)
- **Test Users**: Register via /register/ or create via Django admin

## 📖 Usage Guide

### For Students/Users
1. **Register/Login** at `/register/` or `/login/`
2. **Browse Books** via sidebar → "All Books"
   - Use search bar and filters (category, availability)
   - Toggle between grid and list view
3. **Issue a Book**:
   - Click "Borrow" on book card
   - Request is sent to admin for approval
4. **Manage Loans**:
   - Go to "My Books" to view active/returned issues
   - Renew (extend by 14 days) or view fines
   - Admins finalize returns
5. **Profile**:
   - Click username → "Profile"
   - Update name, phone, address, and avatar

### For Admins
1. **Login as staff user** (is_staff=True)
2. **Access Admin Panel** via navbar → "Admin Panel" or sidebar link
3. **Dashboard**: View key metrics (books, users, issues, fines)
4. **Manage Books**:
   - Add: Fill inline form at top of Books page
   - Edit: Click edit icon → modal opens with pre-filled data
   - Delete: Click trash icon → confirm deletion
5. **Manage Categories**: Similar workflow with modals
6. **Manage Users**:
   - Edit: Update role, name, email, active status
   - Toggle Status: Quick activate/deactivate link
7. **Issue Workflow**:
   - Pending requests appear in admin panel or fines page
   - Approve: Decrements book availability, activates issue
   - Reject: Marks issue as rejected
8. **Fines**: View overdue issues with calculated fines
9. **Reports**: Placeholder for future analytics (filters, PDF export)
10. **Exports**: Download books.csv or issues.csv for offline analysis

## 🔧 Configuration

### Environment Variables (.env)
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1
```

### Settings Highlights
- **Custom User Model**: `AUTH_USER_MODEL = 'users.CustomUser'`
- **Static Files**: Collected to `staticfiles/`, served via Whitenoise in prod
- **Media Files**: `media/` for uploads, can switch to AWS S3 (`USE_S3=True`)
- **Email Backend**: SMTP for Gmail (or use SendGrid, Mailgun in prod)
- **CORS**: Configured for `localhost:3000` (Next.js frontend if needed)
- **JWT**: Simple JWT tokens configured for API authentication

## 🚀 Deployment

### Heroku Deployment
1. Install Heroku CLI and login
2. Create `Procfile`:
   ```
   web: gunicorn library_management.wsgi --log-file -
   ```
3. Add `gunicorn` to `requirements.txt`
4. Set environment variables in Heroku dashboard
5. Deploy:
   ```bash
   git init
   heroku create your-app-name
   git add .
   git commit -m "Initial deploy"
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure Whitenoise or CDN for static files
- [ ] Enable AWS S3 for media uploads
- [ ] Set strong `SECRET_KEY` from environment
- [ ] Configure email backend (SendGrid, AWS SES)
- [ ] Enable HTTPS and update `SECURE_*` settings
- [ ] Set up scheduled tasks for overdue email notifications (cron/Celery)
- [ ] Add monitoring (Sentry for errors)

### Database Migration (SQLite → PostgreSQL)
1. Dump existing data:
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > datadump.json
   ```
2. Update `DATABASES` in settings to PostgreSQL
3. Run migrations on new DB:
   ```bash
   python manage.py migrate
   ```
4. Load data:
   ```bash
   python manage.py loaddata datadump.json
   ```

## 📝 API Documentation

### Authentication
- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/` (returns JWT tokens)
- **Profile**: `GET /api/auth/profile/` (requires authentication)

### Endpoints
- **Books**: `/api/books/` (GET list, POST create)
- **Book Detail**: `/api/books/{id}/` (GET, PUT, DELETE)
- **Categories**: `/api/categories/`
- **Book Issues**: `/api/bookissues/`
- **Reviews**: `/api/reviews/`
- **Reservations**: `/api/reservations/`

Use JWT token in headers: `Authorization: Bearer <access_token>`

## 🧪 Testing

Run Django tests:
```bash
python manage.py test
```

Test coverage (if configured):
```bash
coverage run --source='.' manage.py test
coverage report
```

## 🐛 Troubleshooting

### Common Issues

1. **Migration conflicts after CustomUser**
   - Delete `db.sqlite3`
   - Remove all `__pycache__` folders
   - Run `makemigrations` and `migrate` fresh

2. **Static files not loading**
   - Run `python manage.py collectstatic --clear`
   - Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings
   - Verify cache-bust parameter in templates (`?v=...`)

3. **NoReverseMatch errors**
   - Ensure all URL names match between `urls.py` and templates
   - Check for missing imports in `urls.py`

4. **Email not sending**
   - Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in .env
   - For Gmail, enable "Less secure app access" or use App Password
   - Check `fail_silently=False` to see errors

5. **Profile picture not displaying**
   - Ensure `MEDIA_URL` and `MEDIA_ROOT` are set
   - Check `+ static(settings.MEDIA_URL, ...)` in `urls.py`
   - Verify file upload in form uses `enctype="multipart/form-data"`

## 🔮 Future Enhancements

- [ ] **Email Notifications**: Scheduled alerts for due/overdue books
- [ ] **Advanced Reports**: Filters, charts, PDF generation (ReportLab/WeasyPrint)
- [ ] **Payment Gateway**: Razorpay/Stripe integration for fines
- [ ] **Book Reservations**: Queue system for unavailable books
- [ ] **Reviews & Ratings**: User feedback on books
- [ ] **Barcode Scanning**: QR/barcode for quick issue/return
- [ ] **Mobile App**: React Native or Flutter frontend
- [ ] **Multi-library Support**: Separate tenants/branches
- [ ] **Search Enhancements**: Elasticsearch integration
- [ ] **Notifications**: Real-time via WebSockets (Django Channels)

## 📄 License

This project is for educational and demonstration purposes. Feel free to use, modify, and distribute as needed.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📧 Contact & Support

For questions or issues:
- Create an issue in the repository
- Email: admin@example.com (update with actual contact)
- Documentation: See inline code comments and docstrings

---

**Built with ❤️ using Django | Modern UI with Teal Theme | Separate Admin & User Panels | Production-Ready Architecture**
