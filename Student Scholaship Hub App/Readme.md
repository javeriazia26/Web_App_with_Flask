# ScholarHub – Student Scholarship Portal

ScholarHub is a Flask-based web application developed to manage student scholarships, academic records, and administrative operations. The project was built to strengthen backend development skills while implementing authentication, role-based access control, REST APIs, database management, and web application security.

The system provides two different user roles:

- **Student** – Can view scholarship recipients and filter records by university campus and department.
- **Administrator** – Has full access to manage scholarships, funding sources, universities, departments, students, and academic results through a dedicated admin dashboard.

Every important administrative activity, including login attempts and CRUD operations, is recorded through an audit logging system for better accountability.

---

## Features

### Student

- Register a new account
- Verify email address
- Secure login and logout
- OTP-based password reset
- Access a personalized dashboard
- View scholarship recipients
- Filter scholarship records by campus and department

### Administrator

- Secure administrator dashboard
- Manage scholarships
- Manage funding sources
- Manage universities
- Manage departments
- Manage student records
- Manage academic results
- Full Create, Read, Update, and Delete (CRUD) functionality
- View complete audit logs

## Technologies Used

- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Jinja2
- HTML
- CSS
- JavaScript
- SQLite
- Python-dotenv
- SMTP Email Service

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
│   │   ├── verify.py
│   │   ├── forget_pass.py
│   │   └── admin/
│   ├── services/
│   │   ├── email_service.py
│   │   └── otp_service.py
│   ├── static/
│   │   ├── css/                 
│   │   ├── js/                  
│   │   └── image/               
│   └── templates/
│       ├── auth/                
│       ├── admin/              
│       └── user_dash.html 
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## Database Models

The application uses the following database models:

- **Credential** – Stores user credentials and roles
- **EmailOTP** – Stores OTPs used for verification and password reset
- **AuditLog** – Records administrative actions
- **FundingSource** – Stores scholarship funding organizations
- **Scholarship** – Scholarship information
- **University** – University details
- **Department** – Departments linked to universities
- **Student** – Student profile and enrollment details
- **Result** – Semester-wise CGPA records

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd "Student Scholarship Portal"
```

### Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```


```env
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///instance/scholarship.db

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

> **Note:** If you're using Gmail, generate an App Password instead of using your account password.

> 

### Run the application

```bash
python run.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## How the Application Works

The application follows Flask's application factory pattern and uses Blueprints to organize different modules.

The general workflow is:

1. A user registers an account.
2. An email verification code is sent.
3. After verification, the user can log in.
4. Students access their dashboard to view scholarship-related information.
5. Administrators can manage records through the admin panel.
6. Administrative actions are recorded in audit logs for tracking purposes.

---

## Security Features

The application currently includes:

- Password hashing
- Role-Based Access Control (RBAC)
- Session-based authentication
- Email verification
- OTP-based password reset
- Parameterized SQL queries to reduce SQL injection risks
- REST API implementation
- Audit logging for:
  - User login
  - Record creation
  - Record updates
  - Record deletion

Currently under development:

- Encryption for protecting sensitive application data

## Audit Logging

The application keeps track of important system activities performed by users. Logged events currently include:

- User login
- Record creation
- Record updates
- Record deletion

Each log stores information about the user who performed the action, the affected module, the operation performed, and the timestamp.

---

## REST API

The project includes REST APIs for handling application data and supporting backend operations. These APIs are integrated with the application's authentication and database layers to provide secure and structured data access.

---

## Project Status

The core functionality of ScholarHub has been completed, including authentication, role-based access control, REST APIs, and administrative management features.

The final feature currently under development is encryption for protecting sensitive application data.
