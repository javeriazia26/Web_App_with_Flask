# ScholarHub - Student Scholarship Portal

A Flask-based web application for managing university scholarships, student records, academic results, and funding sources. The system provides separate dashboards for administrators and students, along with role-based access control to ensure secure access to data.

## Project Overview

ScholarHub is designed to simplify scholarship management within a university. Administrators can manage students, scholarships, departments, universities, funding sources, and academic results, while students can log in to view their personal academic and scholarship information.

## Features

### Administrator

* Secure administrator login
* Dashboard with system statistics
* Manage students (Add, Update, Delete)
* Manage scholarships
* Manage funding sources
* Manage departments
* Manage universities
* Record and manage student results (CGPA and semester grades)
* Manage user accounts
* View audit logs of administrative activities

### Student

* Secure login
* View personal profile
* View scholarship information
* View academic results

### Security

* Password hashing using Werkzeug
* Role-Based Access Control (RBAC)
* Session-based authentication
* Server-side validation
* Audit logging for administrative actions

---

## Technology Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy ORM
* SQLite (Development)
* HTML5
* CSS3
* JavaScript
* Jinja2
* Werkzeug

---

## Project Structure

```text
Student Scholarship Portal/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dash.py
│   │   ├── login_form.py
│   │   ├── reg_form.py
│   │   └── admin/
│   │       ├── admin.py
│   │       ├── scholar.py
│   │       ├── std.py
│   │       ├── depart.py
│   │       ├── uni.py
│   │       ├── fund_src.py
│   │       ├── result.py
│   │       └── audit_log.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── image/
│   └── templates/
│       ├── admin/
│       ├── auth/
│       └── user_dash.html
├── instance/
├── run.py
└── README.md
```

---

## Database Models

The application uses the following database models:

* Credential
* Student
* Scholarship
* FundingSource
* Department
* University
* Result
* AuditLog
* Token

These models are connected using SQLAlchemy relationships to maintain data integrity and simplify database operations.

---

## Installation

### Prerequisites

* Python 3.8 or above
* pip
* Virtual environment (recommended)

### Clone the Repository

```bash
git clone <repository-url>
cd "Student Scholarship Portal"
```

### Create a Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create the Database

```python
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
```

### Run the Application

```bash
python run.py
```

The application will be available at:

```
http://localhost:5000
```

---

## Current Features

* User Authentication
* Role-Based Access Control
* CRUD Operations
* Student Management
* Scholarship Management
* Department Management
* University Management
* Funding Source Management
* Academic Result Management
* Audit Logging
* Dashboard Statistics

---

## Future Improvements

Planned improvements include:

* Search and filtering
* Email notifications
* PDF report generation
* Responsive UI improvements
* Two-Factor Authentication (2FA)
* Database migration to MySQL/PostgreSQL
* Encryption for sensitive student information
* REST API for third-party integration

---

## Project Workflow

### Administrator

1. Login
2. Access dashboard
3. Manage system records
4. View audit logs
5. Logout

### Student

1. Register/Login
2. View dashboard
3. View scholarship details
4. View academic results
5. Logout

---

## Screenshots

Screenshots will be added after the user interface is finalized.

---

## Future Documentation

The following documentation will be added in future versions:

* ER Diagram
* Database Schema
* API Documentation
* Deployment Guide

---

## Developer

**Jaweria Zia**

BS Computer Science

---

## Version

**Version:** 0.1.0

**Status:** In Development

**Last Updated:** June 2026

