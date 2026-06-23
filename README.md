# 🎓 College Admission Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python) ![Django](https://img.shields.io/badge/Django-6.0.4-green?logo=django) ![MySQL](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-orange?logo=mysql) ![Razorpay](https://img.shields.io/badge/Payments-Razorpay-blue?logo=razorpay) ![License](https://img.shields.io/badge/License-Internship-lightgrey)

A full-stack web application built with **Django** for managing college admissions end-to-end — from student registration and document upload to payment processing and admin-side allotment management.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Project](#running-the-project)
- [Database Configuration](#database-configuration)
- [Key Modules](#key-modules)
- [URL Routes](#url-routes)
- [Admin Panel](#admin-panel)
- [Deployment](#deployment)

---

## ✨ Features

### Student Portal
- **User Registration & Login** — Secure account creation and session-based authentication
- **Multi-step Application Form** — Personal details → Academic details → Document upload → Course selection
- **Course Browsing** — View available courses with seats and duration
- **Payment Integration** — Razorpay-powered online payment for application fees
- **Dashboard** — Track application status (Pending / Approved / Rejected)
- **PDF Downloads** — Download application slip and allotment slip as PDF

### Admin Panel
- **Admin Registration & Login** — Separate admin authentication system
- **Dashboard** — Overview statistics of students, applications, and payments
- **Student Management** — View, search, and delete student records
- **Application Management** — Review and update application statuses
- **Course Management** — Add and delete courses
- **Payment Records** — View all payment transactions
- **Excel Export** — Export the full student list to Excel (`.xlsx`)

---

## 🛠 Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Python 3.x, Django 6.0.4            |
| Database     | MySQL (production) / SQLite (local) |
| Payments     | Razorpay API                        |
| PDF Reports  | ReportLab                           |
| Excel Export | openpyxl                            |
| Static Files | WhiteNoise                          |
| Deployment   | Gunicorn + Render                   |

---

## 📁 Project Structure

```
college_admission_web/
├── admissionproject/          # Django project root
│   ├── admissionapp/          # Main application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # Business logic & views
│   │   ├── urls.py            # URL routing
│   │   ├── admin.py           # Django admin config
│   │   ├── decorators.py      # Custom auth decorators
│   │   ├── static/            # CSS, JS, images
│   │   ├── templates/         # HTML templates
│   │   └── migrations/        # Database migrations
│   ├── admissionproject/
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # Root URL config
│   │   └── wsgi.py            # WSGI entry point
│   ├── media/                 # User-uploaded files
│   ├── manage.py
│   ├── create_admin.py        # Script to create admin user
│   ├── populate_data.py       # Script to seed sample data
│   └── .env                   # Environment variables
├── environment/               # Python virtual environment
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- MySQL server (for production) **or** SQLite (for local development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd college_admission_web
   ```

2. **Activate the virtual environment**
   ```bash
   # Windows (PowerShell)
   .\environment\Scripts\Activate.ps1

   # Windows (CMD)
   environment\Scripts\activate.bat

   # Linux / macOS
   source environment/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create or update `admissionproject/.env` with the following variables:

```env
# Django
SECRET_KEY=your-secret-key-here

# Database (MySQL — leave blank if using SQLite locally)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306

# Razorpay (get from https://razorpay.com/docs/)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret

# Set to 'true' to use SQLite locally instead of MySQL
USE_SQLITE=true
```

### Running the Project

#### Option A — Local development with SQLite (recommended for local)

```powershell
# Windows PowerShell
$env:USE_SQLITE='true'
.\environment\Scripts\python.exe admissionproject\manage.py migrate
.\environment\Scripts\python.exe admissionproject\manage.py runserver
```

```bash
# Linux / macOS
USE_SQLITE=true python admissionproject/manage.py migrate
USE_SQLITE=true python admissionproject/manage.py runserver
```

Visit: **http://127.0.0.1:8000**

#### Option B — With MySQL

Ensure the MySQL server is accessible and credentials in `.env` are correct, then:

```bash
python admissionproject/manage.py migrate
python admissionproject/manage.py runserver
```

#### Creating an Admin User

```bash
# Using the built-in script
python admissionproject/create_admin.py

# Or use the admin registration page
# http://127.0.0.1:8000/admin-register/
```

#### Seeding Sample Data

```bash
python admissionproject/populate_data.py
```

---

## 🗄 Database Configuration

The project supports two database backends, toggled via the `USE_SQLITE` environment variable:

| `USE_SQLITE` | Database Used                         |
|--------------|---------------------------------------|
| `true`       | SQLite (file: `admissionproject/db.sqlite3`) |
| `false` / unset | MySQL (credentials from `.env`)    |

---

## 🔑 Key Modules

### Models (`admissionapp/models.py`)

| Model            | Description                                      |
|------------------|--------------------------------------------------|
| `Register`       | Stores login credentials for students            |
| `Students`       | Full student profile (personal + contact info)   |
| `AcademicDetails`| 10th / 12th marks and previous institution       |
| `Documents`      | Uploaded documents linked to a student           |
| `Courses`        | Available courses with seats and duration        |
| `Applications`   | Student applications with 1st and 2nd course preference |
| `Payments`       | Razorpay payment records                         |
| `AdminProfile`   | Admin account details                            |

---

## 🌐 URL Routes

### Student-Facing

| URL                          | Description                        |
|------------------------------|------------------------------------|
| `/`                          | Home page                          |
| `/register/`                 | Student sign-up                    |
| `/login/`                    | Student login                      |
| `/courses/`                  | Browse available courses           |
| `/student-register/`         | Personal details form              |
| `/academic-details/`         | Academic details form              |
| `/upload-documents/`         | Document upload                    |
| `/apply/`                    | Submit application                 |
| `/dashboard/`                | Student dashboard                  |
| `/payment/`                  | Payment page                       |
| `/payment/success/`          | Payment confirmation               |
| `/download-application-slip/`| Download application PDF           |
| `/download-allotment-slip/<id>/` | Download allotment PDF         |

### Admin-Facing

| URL                                      | Description                    |
|------------------------------------------|--------------------------------|
| `/admin-login/`                          | Admin login                    |
| `/admin-panel/`                          | Admin home                     |
| `/admin-panel/dashboard/`               | Full stats dashboard           |
| `/admin-panel/students/`                | All students list              |
| `/admin-panel/students/<id>/`           | Student detail view            |
| `/admin-panel/applications/`            | All applications               |
| `/admin-panel/applications/update/<id>/`| Update application status      |
| `/admin-panel/payments/`                | Payment records                |
| `/admin-panel/courses/`                 | Manage courses                 |
| `/admin-panel/export-students-excel/`   | Download student data as Excel |

---

## 🔧 Admin Panel

Django's built-in admin interface is also available at `/django-admin/` (requires a Django superuser):

```bash
python admissionproject/manage.py createsuperuser
```

---

## ☁️ Deployment

This project is configured for deployment on **[Render](https://render.com/)** using **Gunicorn**:

- Static files are served via **WhiteNoise**
- `ALLOWED_HOSTS` includes `.onrender.com`
- Set environment variables in Render's dashboard (same as `.env`)
- Set `USE_SQLITE=false` and configure MySQL credentials in production

**Start command for Render:**
```bash
gunicorn --chdir admissionproject admissionproject.wsgi:application
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project was developed as part of an internship. All rights reserved.
