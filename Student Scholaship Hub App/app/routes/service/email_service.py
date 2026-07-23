import smtplib
from email.message import EmailMessage
from flask import current_app


def send_verification_email(email, otp):
    mail_server = current_app.config["MAIL_SERVER"]
    mail_port = current_app.config["MAIL_PORT"]
    mail_username = current_app.config["MAIL_USERNAME"]
    mail_password = current_app.config["MAIL_PASSWORD"]

    message = EmailMessage()
    message["Subject"] = "Verify Your Email"
    message["From"] = mail_username
    message["To"] = email

    message.set_content(
        f"""
        Hi, {email}
We received your request to verify your email to use student scholarship hub website.
Your verification code is: {otp}

This code will expire in 5 minutes.

If you didn't create this account, please ignore this email.
"""
    )

    try:
        with smtplib.SMTP(mail_server, mail_port) as smtp:
            smtp.starttls()
            smtp.login(mail_username, mail_password)
            smtp.send_message(message)

        return "Verification email sent successfully.", "success"

    except smtplib.SMTPException as e:
        
        return "Unable to send verification email. Please try again later.", "error"

    except Exception as e:
        
        return "An unexpected error occurred while sending the email.", "error"