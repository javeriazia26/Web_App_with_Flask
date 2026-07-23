import secrets, hashlib
from datetime import date, datetime, timedelta
from app.models import Credential, EmailOTP
from app import db


from app.services.email_service import send_verification_email

def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()

def create_otp(user_id, purpose):
    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    
    
    email_otp = EmailOTP(
        user_id=user_id,
        hashed_otp=hashed_otp,
        expires_at=expires_at,
        purpose=purpose
    )

    existing = EmailOTP.query.filter_by(user_id=user_id, purpose=purpose).first()

    try:
        if existing:
            db.session.delete(existing)

        db.session.add(email_otp)
        db.session.commit()
        
        
        

        saved = EmailOTP.query.filter_by(user_id=user_id, purpose=purpose).first()
        

        
        return otp

    except Exception as e:
        
        db.session.rollback()
        return None
    
def verify_otp(user_id, otp, purpose):
    
    record = EmailOTP.query.filter_by(user_id=user_id, purpose=purpose).first()
    
    if record is None:
        return "OTP not found", "error"
        
    if record.expires_at < datetime.utcnow():

        db.session.delete(record)
        db.session.commit()
        return "OTP has expired. Please request a new OTP.", "error"
        
    if record.attempts >= 5:
        db.session.delete(record)
        db.session.commit()
        return "Maximum attempts reached. Please request a new OTP.", "error"
    
    # Check if the provided OTP matches the hashed OTP in the database
    if hash_otp(otp) != record.hashed_otp:
        record.attempts += 1

        if record.attempts >= 5:
            db.session.delete(record)
            db.session.commit()
            return "Maximum attempts reached. Please request a new OTP.", "error"

        db.session.commit()
        return f"Invalid OTP. You have {5 - record.attempts} attempts left.", "error"

    # Correct OTP
    db.session.delete(record)
    db.session.commit()

    return "OTP verified successfully.", "success"
    
def send_resend_otp(user_id, purpose):
    user = db.session.get(Credential, user_id)
    if not user:
        return "User not found.", "error"

    today = date.today()

    if user.otp_last_resend_date == today:
        if user.otp_resend_count >= 2:
            return "You have already reached the maximum resend limit for today.", "error"

    record = EmailOTP.query.filter_by(user_id=user_id, purpose=purpose).first()

    # OTP already exists and is still valid
    if record and record.expires_at > datetime.utcnow():
        return "You already have a valid OTP. Please check your email.", "info"

    # No OTP exists or the existing OTP has expired
    otp = create_otp(user_id, purpose=purpose)

    if otp is None:
        return "Unable to create OTP. Please try again later.", "error"

    message, category = send_verification_email(user.email, otp)

    if category == "error":
        # Delete the OTP because the email wasn't sent
        record = EmailOTP.query.filter_by(user_id=user_id, purpose=purpose).first()
        if record:
            db.session.delete(record)
            db.session.commit()

        return message, category

    # Update resend count
    if user.otp_last_resend_date == today:
        user.otp_resend_count += 1
    else:
        user.otp_resend_count = 1
        user.otp_last_resend_date = today

    db.session.commit()

    return "A new OTP has been sent to your email.", "success"