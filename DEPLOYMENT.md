# Deploying to PythonAnywhere

## Prerequisites
- PythonAnywhere free account (https://www.pythonanywhere.com)
- GitHub repository with your code

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com
- Sign up for free account
- Verify email

### 2. Open Bash Console
- Dashboard → Consoles → Bash

### 3. Clone Repository
```bash
git clone https://github.com/AashishBadhan/library-management.git
cd library-management
```

### 4. Create Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure Environment Variables
```bash
nano .env
```
Add:
```env
DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourusername.pythonanywhere.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 6. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Configure Web App
- Dashboard → Web → Add a new web app
- Choose "Manual configuration"
- Python version: 3.10

### 8. Configure WSGI File
Click on WSGI configuration file and replace with:
```python
import os
import sys

path = '/home/yourusername/library-management'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'library_management.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 9. Set Virtual Environment Path
In Web tab:
- Virtualenv: `/home/yourusername/library-management/venv`

### 10. Configure Static Files
In Web tab → Static files:
- URL: `/static/`
- Directory: `/home/yourusername/library-management/staticfiles`

### 11. Reload Web App
- Click "Reload" button

### 12. Setup Daily Notifications (Optional)
- Dashboard → Tasks
- Add scheduled task:
  - Time: 09:00 (daily)
  - Command: 
    ```bash
    /home/yourusername/library-management/venv/bin/python /home/yourusername/library-management/manage.py send_notifications
    ```

## Testing
Visit: `https://yourusername.pythonanywhere.com`

## Troubleshooting

### Error Logs
Check error logs in Web tab → Log files

### Database Issues
```bash
cd ~/library-management
source venv/bin/activate
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```
Then reload web app

## Important Notes

1. **Free Account Limitations:**
   - One web app only
   - Domain: yourusername.pythonanywhere.com
   - Sleeps after 3 months of inactivity
   - Limited CPU time

2. **Database:**
   - SQLite works on free tier
   - For PostgreSQL, upgrade to paid plan

3. **Email:**
   - Gmail SMTP works fine
   - Ensure "Less secure app access" is enabled or use App Password

4. **Updates:**
   ```bash
   cd ~/library-management
   git pull origin main
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
   Then reload web app from dashboard

## Support
For issues, check PythonAnywhere forums or contact support.
