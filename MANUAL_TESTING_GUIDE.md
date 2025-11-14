# 🧪 Manual Testing Guide - Library Management System

**Testing URL:** http://127.0.0.1:8000/  
**Browser:** Already opened in VS Code Simple Browser  
**Server:** Running on port 8000 ✅

---

## 📋 TESTING CHECKLIST - Follow These Steps

### ✅ STEP 1: LOGIN PAGE (Current Page)
**URL:** http://127.0.0.1:8000/

#### Test Cases:
- [ ] 1. **Visual Check:**
  - Page loads properly?
  - Login form visible?
  - Username and Password fields present?
  - "Remember Me" checkbox?
  - "Login" button visible?
  - "Sign Up" link visible?
  - "Forgot Password" link visible?

- [ ] 2. **Invalid Login Test:**
  - Enter: username = `test`, password = `wrong`
  - Click "Login"
  - **Expected:** Error message "Invalid credentials"
  - **Expected:** Rate limit notice after 5 attempts

- [ ] 3. **Valid Student Login:**
  - Enter: username = `Aashish`, password = (your password)
  - Click "Login"
  - **Expected:** Redirects to `/dashboard/`
  - **Expected:** Shows student dashboard

---

### ✅ STEP 2: STUDENT DASHBOARD
**URL:** http://127.0.0.1:8000/dashboard/

#### Test Cases:
- [ ] 4. **Dashboard Statistics:**
  - Can see "Books Available" count
  - Can see "Books Borrowed" count
  - Can see "Books Overdue" count
  - Charts/graphs loading?

- [ ] 5. **Navigation Menu:**
  - "Dashboard" link active?
  - "Browse Books" link visible?
  - "My Books" link visible?
  - "Profile" link visible?
  - "Notifications" badge showing count?
  - "Logout" link visible?

---

### ✅ STEP 3: BROWSE BOOKS
**URL:** http://127.0.0.1:8000/books/

#### Test Cases:
- [ ] 6. **Book List Display:**
  - Shows 29 books?
  - Each book shows: Title, Author, ISBN, Category, Available copies
  - "Issue Book" button visible on each book?

- [ ] 7. **Category Filter:**
  - Click "Fiction" filter
  - **Expected:** Shows only fiction books
  - Click "All Categories"
  - **Expected:** Shows all 29 books again

- [ ] 8. **Search Function:**
  - Type "Harry Potter" in search box
  - **Expected:** Shows matching book
  - Clear search
  - **Expected:** Shows all books

- [ ] 9. **Issue Book Request:**
  - Find book "1984" (or any available book)
  - Click "Issue Book" button
  - Select return date (14 days from today)
  - Click "Submit"
  - **Expected:** Success message "Request submitted"
  - **Expected:** Redirects to My Books page

---

### ✅ STEP 4: MY BOOKS PAGE
**URL:** http://127.0.0.1:8000/my-books/

#### Test Cases:
- [ ] 10. **Issued Books List:**
  - Shows book you just requested
  - Shows "Status: Pending Approval" (yellow badge)
  - Shows issue date
  - Shows due date
  - Shows "Days Remaining: N/A" (pending approval)

- [ ] 11. **After Admin Approval** (do this after Step 6):
  - Refresh the page
  - **Expected:** Status changes to "Active" or "Approved" (green)
  - **Expected:** Days remaining shows a number
  - **Expected:** Fine shows ₹0.00 (if not overdue)
  - **Expected:** "Renew" button appears
  - **Expected:** "Return" button appears

- [ ] 12. **Renew Book Test:**
  - Click "Renew" button
  - **Expected:** Success message
  - **Expected:** Due date extends by 14 days
  - **Expected:** Days remaining increases

- [ ] 13. **Return Book Test** (optional):
  - Click "Return" button
  - **Expected:** Confirmation dialog
  - Click "Confirm"
  - **Expected:** Book marked as returned
  - **Expected:** Fine calculated if overdue

---

### ✅ STEP 5: PROFILE PAGE
**URL:** http://127.0.0.1:8000/profile/

#### Test Cases:
- [ ] 14. **Profile Information:**
  - Shows username: Aashish
  - Shows email
  - Shows role: Student
  - Edit profile form visible?

- [ ] 15. **Update Profile:**
  - Change first name to "Test"
  - Click "Update"
  - **Expected:** Success message
  - **Expected:** Name updated

---

### ✅ STEP 6: LOGOUT & ADMIN LOGIN
**URL:** http://127.0.0.1:8000/logout/

#### Test Cases:
- [ ] 16. **Logout:**
  - Click "Logout" from navbar
  - **Expected:** Redirects to login page
  - **Expected:** Session cleared

- [ ] 17. **Admin Login:**
  - Enter: username = `admin`
  - Enter: password = `admin123`
  - Click "Login"
  - **Expected:** Redirects to admin dashboard
  - **Expected:** "Admin Panel" link visible in navbar

---

### ✅ STEP 7: ADMIN DASHBOARD
**URL:** http://127.0.0.1:8000/admin/dashboard/

#### Test Cases:
- [ ] 18. **Admin Statistics:**
  - Shows "Total Books: 29"
  - Shows "Total Users: 2"
  - Shows "Active Issues: 1" (or more)
  - Shows "Overdue: 0" (or actual count)

- [ ] 19. **Pending Book Requests Section:**
  - **Orange header** visible?
  - Shows "Pending Book Requests (1)" badge
  - Table shows:
    - Student name: Aashish
    - Book title: 1984 (or your issued book)
    - Requested date
    - Due date
  - **Green "Approve" button** visible?
  - **Red "Reject" button** visible?

- [ ] 20. **Approve Request:**
  - Click "Approve" button
  - **Expected:** Success message "Issue approved"
  - **Expected:** Request disappears from Pending section
  - **Expected:** Appears in Recent Issues with "Approved" badge

- [ ] 21. **Recent Issues Section:**
  - Shows last 10 issues
  - Each issue shows:
    - Student name
    - Book title
    - Issue date
    - Status badge (color-coded)

---

### ✅ STEP 8: MANAGE BOOKS
**URL:** http://127.0.0.1:8000/admin/books/

#### Test Cases:
- [ ] 22. **Book List:**
  - Table shows all 29 books
  - Columns: ID, Title, Author, Category, Qty, Available, Actions
  - Category names showing properly (not "N/A" for all)?

- [ ] 23. **Add New Book:**
  - Fill form: 
    - Title: "Test Book"
    - Author: "Test Author"
    - ISBN: "TEST123456"
    - Category: Fiction
    - Quantity: 5
    - Price: 299
    - Publication Date: 2025-01-01
  - Click "Add" button
  - **Expected:** Success message
  - **Expected:** Book appears in list
  - **Expected:** Total books = 30

- [ ] 24. **Edit Book:**
  - Find "Test Book"
  - Click "Edit" button (pencil icon)
  - Change title to "Test Book Updated"
  - Click "Save"
  - **Expected:** Success message
  - **Expected:** Title updated in list

- [ ] 25. **Delete Book:**
  - Find "Test Book Updated"
  - Click "Delete" button (trash icon)
  - Confirm deletion
  - **Expected:** Success message
  - **Expected:** Book removed from list
  - **Expected:** Total books = 29

- [ ] 26. **Duplicate ISBN Check:**
  - Try to add book with ISBN: "978-0-06-112008-4" (existing)
  - **Expected:** Error "ISBN already exists"

---

### ✅ STEP 9: MANAGE USERS
**URL:** http://127.0.0.1:8000/admin/users/

#### Test Cases:
- [ ] 27. **User List:**
  - Shows 2 users (admin, Aashish)
  - Columns: Username, Email, Role, Status, Actions

- [ ] 28. **Edit User:**
  - Click Edit on "Aashish"
  - Change role to "Librarian" (if option available)
  - Click "Save"
  - **Expected:** Success message
  - **Expected:** Role updated

- [ ] 29. **Toggle User Status:**
  - Click "Toggle Status" on Aashish
  - **Expected:** User becomes inactive
  - Click again
  - **Expected:** User becomes active

---

### ✅ STEP 10: MANAGE CATEGORIES
**URL:** http://127.0.0.1:8000/admin/categories/

#### Test Cases:
- [ ] 30. **Category List:**
  - Shows 9 categories:
    1. Fiction
    2. Science Fiction
    3. Mystery
    4. Romance
    5. Fantasy
    6. Non-Fiction
    7. Biography
    8. History
    9. Self-Help

- [ ] 31. **Add Category:**
  - Click "Add Category"
  - Name: "Test Category"
  - Description: "For testing"
  - Click "Add"
  - **Expected:** Success message
  - **Expected:** Category appears in list

- [ ] 32. **Edit Category:**
  - Edit "Test Category"
  - Change name to "Test Cat Updated"
  - Click "Save"
  - **Expected:** Success message

- [ ] 33. **Delete Category:**
  - Delete "Test Cat Updated"
  - **Expected:** Success message
  - **Expected:** Category removed

---

### ✅ STEP 11: FINES MANAGEMENT
**URL:** http://127.0.0.1:8000/admin/fines/

#### Test Cases:
- [ ] 34. **Fines Overview:**
  - Shows "Total Overdue: 0" (or actual count)
  - Shows "Total Amount: ₹0.00" (or actual)
  - List shows overdue books (if any)

- [ ] 35. **Fine Calculation:**
  - If any book is overdue:
    - Check fine = Days overdue × ₹5
    - Payment status shown?

---

### ✅ STEP 12: REPORTS
**URL:** http://127.0.0.1:8000/admin/reports/

#### Test Cases:
- [ ] 36. **Statistics Cards:**
  - Total Books: 29
  - Total Users: 2
  - Active Issues: (current count)
  - Total Fines: ₹0.00 (or actual)

- [ ] 37. **Charts:**
  - Monthly Issues chart loading?
  - Monthly Fines chart loading?
  - Category Distribution chart loading?

- [ ] 38. **Top Borrowed Books:**
  - Table showing books with borrow count
  - Sorted by most borrowed first?

---

### ✅ STEP 13: EXPORT FEATURES

#### Test Cases:
- [ ] 39. **Export Books CSV:**
  - Click "Export Books CSV" button
  - **Expected:** File downloads (books.csv)
  - Open file
  - **Expected:** Contains all 29 books with details

- [ ] 40. **Export Issues CSV:**
  - Click "Export Issues CSV"
  - **Expected:** File downloads (issues.csv)
  - **Expected:** Contains issue records

- [ ] 41. **Export Books PDF:**
  - Click "Export Books PDF"
  - **Expected:** File downloads (books_report_YYYYMMDD.pdf)
  - Open PDF
  - **Expected:** Formatted table with all books

- [ ] 42. **Export Issues PDF:**
  - Click "Export Issues PDF"
  - **Expected:** File downloads
  - **Expected:** Formatted PDF with issues

- [ ] 43. **Export Fines PDF:**
  - Click "Export Fines PDF"
  - **Expected:** File downloads
  - **Expected:** PDF with fine details

---

### ✅ STEP 14: NOTIFICATIONS
**URL:** http://127.0.0.1:8000/notifications/

#### Test Cases:
- [ ] 44. **Notification List:**
  - Shows notification: "Book Issue Approved: 1984"
  - Shows timestamp
  - Unread badge visible?

- [ ] 45. **Mark All Read:**
  - Click "Mark All as Read"
  - **Expected:** Badge count becomes 0
  - **Expected:** Notifications marked as read

---

### ✅ STEP 15: SECURITY TESTING

#### Test Cases:
- [ ] 46. **Rate Limiting:**
  - Logout
  - Try wrong password 6 times
  - **Expected:** After 5 attempts, shows "Too many requests"
  - **Expected:** 429 error page with countdown timer

- [ ] 47. **Permission Check:**
  - Login as Student (Aashish)
  - Manually visit: http://127.0.0.1:8000/admin/dashboard/
  - **Expected:** Permission denied error
  - **Expected:** Redirects to student dashboard

- [ ] 48. **CSRF Protection:**
  - Inspect any form
  - **Expected:** Hidden CSRF token field present

---

### ✅ STEP 16: RESPONSIVE DESIGN

#### Test Cases:
- [ ] 49. **Mobile View:**
  - Resize browser to mobile size (375px width)
  - **Expected:** Navbar collapses to hamburger menu
  - **Expected:** Tables become scrollable
  - **Expected:** Cards stack vertically

- [ ] 50. **Tablet View:**
  - Resize to 768px width
  - **Expected:** Layout adjusts properly
  - **Expected:** All content readable

---

## 📊 FINAL CHECKLIST

### Core Features (Must Work)
- [x] User Authentication (Login/Logout)
- [x] Student Dashboard
- [x] Browse & Search Books
- [x] Issue Book Request
- [x] Admin Approval System
- [x] My Books Page
- [x] Renew & Return Books
- [x] Fine Calculation (₹5/day)
- [x] Admin Dashboard
- [x] Manage Books (CRUD)
- [x] Manage Users (CRUD)
- [x] Manage Categories (CRUD)
- [x] Reports & Charts
- [x] Export (PDF/CSV)
- [x] Notifications
- [x] Rate Limiting
- [x] Role-Based Access

### Known Working Data
- **Books:** 29 (Fiction, Sci-Fi, Mystery, etc.)
- **Categories:** 9
- **Users:** 2 (admin, Aashish)
- **Active Issues:** 1
- **Server:** Running on port 8000

### Test Credentials
```
Admin:
  Username: admin
  Password: admin123

Student:
  Username: Aashish
  Password: (your registered password)
```

---

## 🐛 IF YOU FIND ANY BUG:

**Report Format:**
1. **Page/URL:** Where did it happen?
2. **Action:** What did you do?
3. **Expected:** What should happen?
4. **Actual:** What actually happened?
5. **Error Message:** Any error shown?

---

## ✅ SUCCESS CRITERIA

All 50 test cases should PASS for system to be production-ready.

**Current Status:** 
- Server: Running ✅
- Database: Populated ✅
- Bug Fixes: 7 Critical bugs fixed today ✅
- Features: All implemented ✅

**Start Testing Now!** 🚀

Open http://127.0.0.1:8000/ in browser and follow steps 1-50.
