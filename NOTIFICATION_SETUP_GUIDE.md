# Automatic Notification System Setup Guide

## Overview
The notification system automatically sends email and in-app notifications to users for:
- 📅 **2 Days Before**: Early reminder that book is due soon
- ⚠️ **1 Day Before**: Urgent reminder - book due tomorrow
- 🚨 **On Due Date**: Final notice - return today to avoid fines
- ⛔ **After Due Date**: Overdue notice with fine calculation (₹5/day)

---

## Windows Task Scheduler Setup

### Step 1: Open Task Scheduler
1. Press `Win + R`
2. Type `taskschd.msc` and press Enter
3. Click "Create Basic Task..." in the right panel

### Step 2: Create the Task
**Name:** Library Notification System
**Description:** Daily notifications for book due dates and overdue fines

### Step 3: Set Trigger
- **Frequency:** Daily
- **Start Date:** Today
- **Time:** 9:00 AM (or your preferred time)
- **Recur every:** 1 day

### Step 4: Set Action
- **Action:** Start a program
- **Program/script:** Browse and select:
  ```
  c:\Users\qq\Desktop\Libraray Management Project completed\Web-Application\run_daily_notifications.bat
  ```
- **Start in:** Leave blank (handled by the batch file)

### Step 5: Finish
- Check "Open Properties dialog" before clicking Finish
- In Properties:
  - Under "General" tab:
    - Check "Run whether user is logged on or not"
    - Check "Run with highest privileges"
  - Under "Conditions" tab:
    - Uncheck "Start the task only if the computer is on AC power"
    - Check "Wake the computer to run this task" (optional)
  - Under "Settings" tab:
    - Check "Run task as soon as possible after a scheduled start is missed"
    - Check "If the task fails, restart every: 10 minutes"
- Click OK

### Step 6: Test the Task
1. Right-click on your new task in Task Scheduler
2. Click "Run"
3. Check if notifications are sent (check terminal output)

---

## Manual Testing

### Test the notification system manually:
```bash
cd "c:\Users\qq\Desktop\Libraray Management Project completed\Web-Application"
python manage.py send_notifications
```

### Expected Output:
```
Checking for due and overdue books...
✓ Sent 2-day reminder to user@email.com
✓ Sent urgent 1-day reminder to user@email.com
✓ Sent FINAL notice to user@email.com
✓ Sent overdue notice to user@email.com (₹25)

📊 Summary:
  • 2 days before: 3
  • 1 day before: 2
  • Due today: 1
  • Overdue: 5
```

---

## Notification Types

### 1. Two Days Before Due Date
- **Email Subject:** "Reminder: Book "[Title]" Due in 2 Days"
- **In-App Title:** "Book Due in 2 Days: [Title]"
- **Icon:** 📅 Info (Blue)

### 2. One Day Before Due Date
- **Email Subject:** "⚠️ Urgent: Book "[Title]" Due Tomorrow"
- **In-App Title:** "⚠️ Due Tomorrow: [Title]"
- **Icon:** ⚠️ Warning (Orange)

### 3. On Due Date
- **Email Subject:** "🚨 FINAL NOTICE: Book "[Title]" Due TODAY"
- **In-App Title:** "🚨 DUE TODAY: [Title]"
- **Icon:** 🚨 Danger (Red)

### 4. Overdue (Daily Reminders)
- **Email Subject:** "⛔ OVERDUE NOTICE: Book "[Title]" - ₹[Fine] Fine"
- **In-App Title:** "⛔ OVERDUE: [Title]"
- **Fine Calculation:** ₹5 per day
- **Icon:** ⛔ Danger (Red)

---

## Viewing Notifications

### In-App Notifications
1. Click the bell icon (🔔) in the top navigation bar
2. See unread count badge
3. View recent notifications in dropdown
4. Click "View All Notifications" for full history

### Email Notifications
- Sent to the user's registered email address
- Check spam folder if not received
- Configure SMTP settings in `.env` file

---

## Email Configuration

### Update `.env` file with your email settings:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `EMAIL_HOST_PASSWORD`

---

## Troubleshooting

### Issue: No emails sent
**Solution:**
- Check `.env` email configuration
- Verify SMTP credentials
- Check user email addresses in database
- Look for error messages in command output

### Issue: Task Scheduler not running
**Solution:**
- Ensure Task Scheduler service is running
- Check task history in Task Scheduler
- Verify batch file path is correct
- Run manually first to test

### Issue: Notifications not appearing in app
**Solution:**
- Check database for Notification records:
  ```bash
  python manage.py shell
  >>> from books.models import Notification
  >>> Notification.objects.all()
  ```
- Clear browser cache and refresh

### Issue: Wrong notification timing
**Solution:**
- Verify Task Scheduler trigger time
- Check server timezone in Django settings
- Adjust `TIME_ZONE` in `settings.py` if needed

---

## Fine Calculation Details

### Automatic Fine System:
- **Base Rate:** ₹5 per day
- **Calculation:** (Days Overdue) × ₹5
- **Example:**
  - 1 day overdue = ₹5
  - 7 days overdue = ₹35
  - 30 days overdue = ₹150

### Display:
- Shown in "My Books" page
- Included in overdue notifications
- Visible in Admin Fines page

---

## Testing Scenarios

### Scenario 1: Book due in 2 days
1. Create a book issue with return_date = today + 2 days
2. Run: `python manage.py send_notifications`
3. Check email and in-app notification

### Scenario 2: Book due tomorrow
1. Create a book issue with return_date = tomorrow
2. Run command
3. Verify urgent notification received

### Scenario 3: Book due today
1. Create a book issue with return_date = today
2. Run command
3. Verify final notice received

### Scenario 4: Book overdue
1. Create a book issue with return_date in the past
2. Run command
3. Verify overdue notice with correct fine amount

---

## Maintenance

### Logs
- Task Scheduler maintains execution logs
- Check: Task Scheduler → Task → History tab

### Database Cleanup
- Old notifications can be cleaned periodically:
  ```bash
  python manage.py shell
  >>> from books.models import Notification
  >>> from datetime import timedelta
  >>> from django.utils import timezone
  >>> cutoff = timezone.now() - timedelta(days=90)
  >>> Notification.objects.filter(created_at__lt=cutoff, is_read=True).delete()
  ```

### Performance
- Notification command runs quickly (< 1 second for 100 users)
- Email sending may take longer (depends on SMTP server)
- Consider async task queue (Celery) for large scale

---

## Success!
✅ Your notification system is now automated and will run daily!
✅ Users will receive timely reminders for due dates
✅ Fines are automatically calculated for overdue books
✅ Email + In-app notifications ensure users never miss a deadline
