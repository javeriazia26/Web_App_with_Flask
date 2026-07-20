from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import University
from app.routes.admin.admin import admin_required, log_action  # shared helper

uni_bp = Blueprint('university', __name__)


# LIST all universities
@uni_bp.route('/admin/uni')
def uni():
    denied = admin_required()
    if denied:
        return denied

    all_universities = University.query.all()
    edit_id = request.args.get('edit')
    editing_university = None
    if edit_id:
        editing_university = University.query.get(edit_id)

    return render_template('admin/uni.html',
        university=all_universities,
        editing_university=editing_university
    )


# ADD university
@uni_bp.route('/admin/uni/add', methods=['POST'])
def add_uni():
    denied = admin_required()
    if denied:
        return denied

    uni_name     = request.form.get('uni_name')
    c_name       = request.form.get('c_name')
    uni_phone_no = request.form.get('uni_phone_no')
    uni_location = request.form.get('uni_location')

    # Duplicate check
    existing_uni = University.query.filter_by(c_name=c_name).first()
    if existing_uni:
        flash(f'A campus with the name "{c_name}" already exists in the system.', "error")
        return redirect(url_for('university.uni'))

    new_uni = University(
        uni_name     = uni_name,
        c_name       = c_name,
        uni_phone_no = uni_phone_no,
        uni_location = uni_location
    )

    db.session.add(new_uni)
    db.session.commit()
    log_action('Added', 'University')

    flash(f'"{uni_name}" campus has been added successfully.', "success")
    return redirect(url_for('university.uni'))


# EDIT university
@uni_bp.route('/admin/uni/edit/<int:uni_id>', methods=['GET', 'POST'])
def edit_uni(uni_id):
    denied = admin_required()
    if denied:
        return denied

    university = University.query.get_or_404(uni_id)

    if request.method == 'POST':
        university.uni_name     = request.form.get('uni_name')
        university.c_name       = request.form.get('c_name')
        university.uni_phone_no = request.form.get('uni_phone_no')
        university.uni_location = request.form.get('uni_location')

        db.session.commit()
        log_action('Updated', 'University')
        flash(f'"{university.uni_name}" details have been updated successfully.', "success")
        return redirect(url_for('university.uni'))

    return redirect(url_for('university.uni'))


# DELETE university
@uni_bp.route('/admin/uni/delete/<int:uni_id>', methods=['POST'])
def delete_uni(uni_id):
    denied = admin_required()
    if denied:
        return denied

    university = University.query.get_or_404(uni_id)
    uni_name   = university.uni_name

    db.session.delete(university)
    db.session.commit()
    log_action('Deleted', 'University')

    flash(f'"{uni_name}" has been permanently removed from the system.', "error")
    return redirect(url_for('university.uni'))