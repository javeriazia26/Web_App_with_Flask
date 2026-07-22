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
