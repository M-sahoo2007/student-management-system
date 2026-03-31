# Admin Panel Setup & Permissions Guide

## Overview
The Student Management System includes a comprehensive Django admin panel with full CRUD permissions and custom bulk actions for administrators.

## 🔐 Admin Access & Permissions

### Quick Setup (Automatic)
Run this command to set up admin permissions:

```bash
python manage.py setup_admin_permissions
```

This will:
- ✓ Create an "Administrators" group with all system permissions
- ✓ Enable full admin access for system managers

### Promote an Existing User to Admin

```bash
python manage.py setup_admin_permissions --username <username>
```

**Example:**
```bash
python manage.py setup_admin_permissions --username john_admin
```

This will:
- ✓ Make the user a **superuser** (full system access)
- ✓ Enable staff privileges
- ✓ Authorize all admin actions
- ✓ Add them to the "Administrators" group

---

## 📋 Admin Features

### Available Actions in Admin Panel

#### 👥 User Management
- **View all users** with roles (Student, Teacher, Admin)
- **Create new users** with specific roles
- **Edit user details** (name, email, roles, permissions)
- **Delete users** (single or bulk)
- **Custom Actions:**
  - ✓ Mark selected as AUTHORIZED
  - ✗ Mark selected as UNAUTHORIZED
  - ↑ Promote selected to ADMIN
  - ↓ Remove ADMIN status

#### 📚 Student Management
- **View all students** with search and filters
- **Create new student records** with personal/academic info
- **Edit student details** (organized in fieldsets)
- **Delete students** (single or bulk)
- **Advanced Filters:** Gender, Class, Section, Joining Date

#### 👨‍🏫 Teacher Management
- **View all teachers** with department and contact info
- **Create new teacher profiles** with hierarchical data
- **Edit teacher information** (Personal, Department, Contact)
- **Delete teachers** (single or bulk)
- **Department Assignment:** Link teachers to specific departments

#### 🏫 Department Management
- **View all departments** with HOD information
- **Create new departments** with contact details
- **Edit department info** (Name, ID, Mobile, HOD)
- **Delete departments** (single or bulk)
- **Department Leadership:** Assign HOD (Head of Department)

#### 📖 Subject Management
- **View all subjects** with department relationships
- **Create new subjects** linked to departments
- **Edit subject details** (Name, ID, Department)
- **Delete subjects** (single or bulk)

#### 🔔 Notification Management
- **View all system notifications** with read status
- **Custom Actions:**
  - ✓ Mark selected as READ
  - ✗ Mark selected as UNREAD
  - Delete unhelpful notifications

#### 🛡️ Password Reset Management
- **Monitor password reset requests** with token validity
- **View user, email, and token information**
- **Check token expiration status**

---

## 🚀 Accessing the Admin Panel

1. **Navigate to:** `http://127.0.0.1:8000/admin/`
2. **Login** with your admin credentials
3. **Select any model** from the admin dashboard
4. **Use search, filters, and actions** to manage data

---

## ⚙️ Admin Fieldsets Organization

Each admin interface is organized into logical sections:

### Students
- Personal Information (Name, Gender, DOB, Religion)
- Student Details (ID, Class, Section, Joining Date, Admission #)
- Contact (Mobile, Parent)
- Media (Student Image)
- System (Slug)

### Teachers
- Personal Information (Name, Gender, DOB, Religion)
- Teacher Details (ID, Department, Joining Date)
- Contact (Mobile, Email, Parent)
- Media (Teacher Image)
- System (Slug)

### Departments
- Department Information (Name, ID)
- Contact (Mobile, Email)
- Leadership (HOD Assignment)
- Media (Department Image)
- System (Slug)

### Subjects
- Subject Information (Name, ID, Department)
- Department (Relationship)
- Media (Subject Image)
- System (Slug)

---

## 🔍 Search & Filter Capabilities

**Example Searches:**
- Find a student: Search by "John" (first name or last name)
- Find a teacher: Search by teacher ID or email
- Find a department: Search by name or ID
- Find notifications: Search by username or message

**Filter Examples:**
- Students: Filter by gender, class, section, or joining date
- Teachers: Filter by gender, department, or joining date
- Notifications: Filter by read status or creation date

---

## ⚠️ Important Notes

- **Superusers** have unrestricted access to all admin features
- **Staff users** need specific permissions granted (handled by `setup_admin_permissions`)
- **Changes made in admin** are immediately reflected in the system
- **Delete operations** cannot be undone - use with caution
- **Bulk actions** apply to all selected items at once

---

## 🆘 Troubleshooting

### "Permission Denied" Error
Run: `python manage.py setup_admin_permissions --username <your_username>`

### Actions Not Showing
Ensure user is staff/superuser and has correct permissions

### Search Not Working
Check that `search_fields` are configured for that model in admin.py

---

## 📞 Support
For issues with the admin panel, contact the system administrator or check Django admin documentation.
