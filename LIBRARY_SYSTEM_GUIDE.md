# 📚 Library Management System - Complete Guide

## 🎯 System Features

### 1. Books Management
- ✅ Add/Edit/Delete Books
- ✅ Track Availability (In Stock/Issued)
- ✅ ISBN Duplicate Prevention
- ✅ Categories
- ✅ Book Images

### 2. Borrow/Issue System (NO BUY OPTION)
- ✅ **Borrow Only** - Students can only borrow books, NOT buy
- ✅ **Issue Duration** - Default 14 days (2 weeks)
- ✅ **Due Date** - Automatically calculated
- ✅ **Return Books** - Admin marks books as returned
- ✅ **Renewal** - Can be extended (if implemented)

### 3. Fine System (Fully Automated)

#### How Fine Works:
```
Fine Rate: ₹5 per day (overdue)
Calculation: Automatic
Payment Status: Tracked (Paid/Unpaid/Overdue)
```

#### Fine Calculation Logic:
```python
# If book returned LATE:
overdue_days = actual_return_date - due_date
fine_amount = overdue_days × ₹5

# Example:
Due Date: Jan 1, 2025
Return Date: Jan 5, 2025
Overdue: 4 days
Fine: 4 × ₹5 = ₹20
```

#### Fine Status:
- **No Fine** - Returned on time
- **Overdue** - Fine calculated, not paid
- **Paid** - Fine cleared
- **Unpaid** - Fine pending

---

## 📝 How to Add Books (Admin)

### Step 1: Login as Admin
1. Go to: http://127.0.0.1:8000/login/
2. Username: `admin`
3. Password: (your admin password)

### Step 2: Add Book
1. Click **"Books"** in sidebar
2. Click **"Add Book"** button
3. Fill form:
   ```
   Title: Harry Potter and the Sorcerer's Stone
   Author: J.K. Rowling
   ISBN: 978-0-439-70818-8
   Category: Fiction
   Quantity: 5
   Publication Year: 1997
   Description: A magical adventure...
   ```
4. Click **"Save"**

### Step 3: View Books
- Books list will show all added books
- Status: **Available** / **Issued**
- Quantity remaining

---

## 🎓 How Students Borrow Books

### Step 1: Student Login
1. Register: http://127.0.0.1:8000/register/
2. Fill details (auto set as 'student' role)
3. Login with credentials

### Step 2: Browse Books
1. Dashboard → **"Browse Books"**
2. Search by title/author/ISBN
3. Filter by category
4. View book details

### Step 3: Request Book
1. Click on book
2. Click **"Issue Book"** or **"Request"**
3. Admin approves request
4. Book issued for **14 days**

### Step 4: Due Date
```
Issue Date: Jan 1, 2025
Due Date: Jan 15, 2025 (14 days later)
Status: Issued
```

---

## ⚠️ Fine System Details

### When Fine is Applied:

#### Scenario 1: On Time Return
```
Issue Date: Jan 1
Due Date: Jan 15
Return Date: Jan 14
Fine: ₹0 ✅
```

#### Scenario 2: Late Return
```
Issue Date: Jan 1
Due Date: Jan 15
Return Date: Jan 20 (5 days late)
Fine: 5 × ₹5 = ₹25 ❌
Status: Overdue
```

#### Scenario 3: Very Late Return
```
Issue Date: Jan 1
Due Date: Jan 15
Return Date: Feb 5 (21 days late)
Fine: 21 × ₹5 = ₹105 ❌❌
Status: Overdue
```

### Fine Payment:
1. Student sees fine amount in dashboard
2. Admin marks fine as "Paid" after payment
3. Payment status updates
4. Student can borrow again

---

## 📊 Admin Dashboard Features

### Books Statistics:
- Total Books
- Books Available
- Books Issued
- Overdue Books

### Issue Management:
- View all issued books
- See due dates
- Mark as returned
- Calculate fines automatically

### Fine Management:
- View all fines
- Total fines collected
- Pending fines
- Mark as paid

### Reports:
- Books report (PDF)
- Issues report (PDF)
- Fines report (PDF)
- Charts & statistics

---

## 🔍 Fine Tracking

### Student View:
```
My Issued Books:
┌─────────────────────────────────────────┐
│ Book: Harry Potter                      │
│ Issue Date: Jan 1                       │
│ Due Date: Jan 15                        │
│ Days Left: 3 days                       │
│ Fine: ₹0 (on time)                      │
└─────────────────────────────────────────┘

Overdue Books:
┌─────────────────────────────────────────┐
│ Book: Lord of the Rings                 │
│ Issue Date: Dec 1                       │
│ Due Date: Dec 15                        │
│ Days Overdue: 5 days ⚠️                 │
│ Fine: ₹25 (unpaid)                      │
└─────────────────────────────────────────┘
```

### Admin View:
```
Fines Summary:
- Total Fines: ₹500
- Paid: ₹300
- Unpaid: ₹200
- Overdue Books: 8
```

---

## 🎮 Quick Test Guide

### 1. Create Admin (if not exists):
```bash
cd Web-Application
python manage.py createsuperuser
# Username: admin
# Email: admin@library.com
# Password: admin123
```

### 2. Add Sample Books:
```
Book 1:
- Title: The Great Gatsby
- Author: F. Scott Fitzgerald
- ISBN: 978-0-7432-7356-5
- Quantity: 3

Book 2:
- Title: 1984
- Author: George Orwell
- ISBN: 978-0-452-28423-4
- Quantity: 5

Book 3:
- Title: To Kill a Mockingbird
- Author: Harper Lee
- ISBN: 978-0-06-112008-4
- Quantity: 2
```

### 3. Create Student Account:
```
Register → Login → Browse Books → Request Book
```

### 4. Issue Book (Admin):
```
Admin Panel → Issues → Approve Request
→ Book issued for 14 days
```

### 5. Test Fine System:
```
Method 1: Wait 14+ days (real time)
Method 2: Manually change due_date in database (testing)
Method 3: Admin marks return with late date
```

---

## 💡 Key Points

### ✅ What's Working:
1. **Borrow System** - Issue/Return books
2. **No Buy Option** - Only borrow, no purchase
3. **Automatic Fines** - ₹5 per overdue day
4. **Fine Tracking** - Paid/Unpaid status
5. **Notifications** - Overdue alerts
6. **Reports** - PDF exports with fine details

### ⚙️ Configuration:
Fine rate can be changed in code:
```python
# books/models.py line 90
self.fine_amount = overdue_days * 5  # Change 5 to any amount
```

### 🎯 Default Settings:
- **Issue Duration**: 14 days (2 weeks)
- **Fine Rate**: ₹5 per day
- **Fine Currency**: ₹ (Rupees)
- **Auto Calculate**: Yes
- **Payment Tracking**: Yes

---

## 🚀 Start Testing

1. **Start Server**:
   ```bash
   cd Web-Application
   python manage.py runserver
   ```

2. **Open Browser**:
   http://127.0.0.1:8000

3. **Login as Admin** → Add Books

4. **Register Student** → Borrow Books

5. **Test Fine System** → Return late

---

**System Complete with:**
- ✅ Borrow (NO Buy)
- ✅ Fine System (₹5/day)
- ✅ 14 Days Duration
- ✅ Auto Calculate
- ✅ Payment Tracking

Happy Testing! 🎉
