from app import create_app
from app.models import Student
from app.services.encryption_service import decrypt_data

app = create_app()

with app.app_context():
    students = Student.query.all()

    for student in students:
        print("-" * 50)
        print(f"Student ID : {student.std_id}")
        print(f"Name       : {student.first_name} {student.last_name}")
        print(f"CNIC       : {decrypt_data(student.encrypted_cnic)}")
        print(f"Phone      : {decrypt_data(student.encrypted_phone)}")