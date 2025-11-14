@echo off
REM Daily Notification Scheduler for Library Management System
REM This script sends notifications for due and overdue books
REM Schedule this with Windows Task Scheduler to run daily at 9:00 AM

echo ====================================
echo Library Management System
echo Daily Notification Scheduler
echo ====================================
echo.

REM Change to Web-Application directory
cd /d "c:\Users\qq\Desktop\Libraray Management Project completed\Web-Application"

REM Activate virtual environment if exists
if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ..\venv\Scripts\activate.bat
)

REM Run the notification command
echo.
echo Running notification system...
python manage.py send_notifications

REM Log completion
echo.
echo ====================================
echo Notification check completed at %date% %time%
echo ====================================
echo.

REM Keep window open for 5 seconds to see results
timeout /t 5

exit
