# Security Setup Guide

## Environment Variables Configuration

### Step 1: Configure .env File

The `.env` file is already created but needs to be configured with your actual values.

**IMPORTANT:** Never commit the `.env` file to version control. It's already in `.gitignore`.

### Step 2: Generate Django Secret Key

Run this command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and replace `DJANGO_SECRET_KEY` in `.env`:

```
DJANGO_SECRET_KEY=your-generated-secret-key-here
```

### Step 3: Configure Email Settings

For Gmail, you need to use an App Password (not your regular password):

1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Generate an App Password: https://support.google.com/accounts/answer/185833
4. Update `.env`:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-app-password
```

### Step 4: Security Features Implemented

#### Rate Limiting (Brute Force Protection)
- **Login**: 5 attempts per minute per IP
- **Registration**: 5 attempts per minute per IP
- **Password Reset**: 5 attempts per minute per IP
- Custom 429 error page shown when rate limit exceeded

#### Production Security Headers (Auto-enabled when DEBUG=False)
- ✅ **HTTPS Redirect**: Forces all traffic to use HTTPS
- ✅ **Secure Cookies**: SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE
- ✅ **HSTS**: HTTP Strict Transport Security (1 year)
- ✅ **XSS Protection**: X-Content-Type-Options and X-Frame-Options
- ✅ **Session Security**: HttpOnly cookies, 24-hour timeout

#### Password Requirements
- Minimum length: 8 characters
- Similarity check (not too similar to user info)
- Common password check
- Numeric-only password prevention

### Step 5: Testing Security Features

#### Test Rate Limiting:
1. Go to the login page
2. Try to login with wrong credentials more than 5 times
3. You should see: "Too many login attempts. Please try again in a few minutes."
4. Wait 60 seconds and try again

#### Test Password Requirements:
1. Go to registration page
2. Try password "12345" - should be rejected (too common)
3. Try password "password" - should be rejected (too common)
4. Try password "Test@123" - should work (8+ chars, not common)

### Step 6: Production Deployment Checklist

When deploying to production:

1. **Update .env**:
   ```
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Setup SSL Certificate**:
   - Use Let's Encrypt or your hosting provider
   - Security headers will auto-enable when DEBUG=False

3. **Database** (Optional - PostgreSQL recommended):
   ```
   DB_NAME=library_db
   DB_USER=postgres
   DB_PASSWORD=strong-password-here
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

### Step 7: Security Monitoring

Monitor these logs for security issues:

- Failed login attempts (check Django logs)
- Rate limit violations (429 errors)
- Suspicious activity patterns

### Configuration Files

- `.env` - Your environment variables (DO NOT COMMIT)
- `.env.example` - Template with examples (safe to commit)
- `settings.py` - Uses python-decouple to load .env values

### Troubleshooting

**Issue**: Rate limiting not working
- **Solution**: Make sure django-ratelimit is installed: `pip install django-ratelimit`
- Check MIDDLEWARE in settings.py includes: `'django_ratelimit.middleware.RatelimitMiddleware'`

**Issue**: Email not sending
- **Solution**: 
  - Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env
  - For Gmail, use App Password, not regular password
  - Check firewall allows port 587

**Issue**: HTTPS redirect causing issues in development
- **Solution**: Keep DEBUG=True in development
- Security headers only activate when DEBUG=False

### Security Best Practices

1. ✅ Never commit `.env` to version control
2. ✅ Use strong, unique passwords for all accounts
3. ✅ Rotate secret keys regularly in production
4. ✅ Monitor failed login attempts
5. ✅ Keep Django and dependencies updated
6. ✅ Use HTTPS in production (required for secure cookies)
7. ✅ Regular security audits and dependency updates

### Additional Resources

- Django Security: https://docs.djangoproject.com/en/stable/topics/security/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Python Decouple: https://github.com/HBNetwork/python-decouple
- Django Ratelimit: https://django-ratelimit.readthedocs.io/

---

**Last Updated**: Security Hardening Implementation
**Version**: 1.0.0
