# Verification Routes
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash

from app import db
from app.models import Credential, EmailOTP
from app.services.otp_service import send_resend_otp, verify_otp

verify_bp = Blueprint("verify", __name__)


# Email Verification
@verify_bp.route("/verify", methods=["GET", "POST"])
def verify():
    if "pending_user_id" not in session:
        flash("No pending verification found.", "error")
        return redirect(url_for("auth.login"))

    user = db.session.get(Credential, session["pending_user_id"])

    if request.method == "POST":
        otp = request.form.get("otp")

        if not user:
            flash("User not found.", "error")
            session.pop("pending_user_id", None)
            return redirect(url_for("auth.login"))

        message, category = verify_otp(user.id, otp, "email-verification")

        if category == "success":
            user.verified = True
            db.session.commit()

            session["user_id"] = user.id
            session["username"] = user.username
            session.pop("pending_user_id", None)

            flash(message, category)

            if user.role == "admin":
                return redirect(url_for("dash.admin_dash"))

            return redirect(url_for("dash.user_dash"))

        flash(message, category)

    record = EmailOTP.query.filter_by(user_id=user.id, purpose="email-verification").first()

    expired = False
    if record and record.expires_at <= datetime.utcnow():
        expired = True

    return render_template(
        "verify.html",
        email=user.email,
        expired=expired,
        resend_url=url_for("verify.resend_otp")
    )


@verify_bp.route("/verify/resend", methods=["POST"])
def resend_otp():
    if "pending_user_id" not in session:
        flash("No pending verification found.", "error")
        return redirect(url_for("auth.login"))

    message, category = send_resend_otp(session["pending_user_id"], purpose="email-verification")
    flash(message, category)

    return redirect(url_for("verify.verify"))


# Password Reset
@verify_bp.route("/verify/reset", methods=["GET", "POST"])
def send_reset_otp():
    if "reset_user_id" not in session:
        flash("No pending password reset found.", "error")
        return redirect(url_for("auth.login"))

    message, category = send_resend_otp(session["reset_user_id"], purpose="password-reset")
    flash(message, category)

    return redirect(url_for("verify.verify_reset_otp"))


@verify_bp.route("/verify/reset_otp", methods=["GET", "POST"])
def verify_reset_otp():
    if "reset_user_id" not in session:
        flash("No pending password reset found.", "error")
        return redirect(url_for("auth.login"))

    user = db.session.get(Credential, session["reset_user_id"])

    if request.method == "POST":
        otp = request.form.get("otp")

        if not user:
            session.pop("reset_user_id", None)
            flash("User not found.", "error")
            return redirect(url_for("auth.forgot_password"))
            

        message, category = verify_otp(user.id, otp, "password-reset")

        if category == "success":
            session["allow_password_reset"] = True
            return redirect(url_for("verify.reset_password"))

        flash(message, category)

    record = EmailOTP.query.filter_by(user_id=user.id, purpose="password-reset").first()

    expired = False
    if record and record.expires_at <= datetime.utcnow():
        expired = True

    return render_template(
        "verify.html",
        email=user.email,
        expired=expired, 
        resend_url=url_for("verify.send_reset_otp")
    )


@verify_bp.route("/verify/reset_password", methods=["GET", "POST"])
def reset_password():
    if "reset_user_id" not in session:
        flash("No pending password reset found.", "error")
        return redirect(url_for("auth.forgot_password"))

    if "allow_password_reset" not in session:
        flash("Please verify the OTP first.", "error")
        return redirect(url_for("verify.verify_reset_otp"))

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("verify.reset_password"))

        user = db.session.get(Credential, session["reset_user_id"])

        if not user:
            flash("Unable to reset password. Please start again.", "error")
            session.pop("reset_user_id", None)
            return redirect(url_for("auth.forgot_password"))

        user.hashed_password = generate_password_hash(password)
        db.session.commit()

        session.pop("reset_user_id", None)
        session.pop("allow_password_reset", None)

        flash("Password reset successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_pass.html")