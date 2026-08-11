from app import create_app, db
from app.models import Student
from app.services.encryption_service import encrypt_data, hash_data

app = create_app()

with app.app_context():
    students = Student.query.all()

    for student in students:
        student.encrypted_cnic = encrypt_data(student.cnic)
        student.cnic_hash = hash_data(student.cnic)

        student.encrypted_phone = encrypt_data(student.std_phone_no)
        student.phone_hash = hash_data(student.std_phone_no)

    db.session.commit()

    print(f"{len(students)} students updated successfully.")