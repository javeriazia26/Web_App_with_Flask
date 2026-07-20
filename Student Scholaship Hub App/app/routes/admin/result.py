from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Result, Student
from app.routes.admin.admin import admin_required, log_action   # shared helper

result_bp = Blueprint('result', __name__)


# LIST all results
@result_bp.route('/admin/result')
def result():
    denied = admin_required()
    if denied:
        return denied

    all_results  = Result.query.all()
    all_students = Student.query.all()
    
    edit_id = request.args.get('edit')
    editing_result = None
    if edit_id:
        editing_result = Result.query.get(edit_id)

    return render_template('admin/result.html',
        results=all_results,
        students=all_students,
        editing_result=editing_result
    )


# ADD result
@result_bp.route('/admin/result/add', methods=['POST'])
def add_result():
    denied = admin_required()
    if denied:
        return denied

    semester = request.form.get('semester')
    cgpa     = request.form.get('cgpa')
    std_id   = request.form.get('std_id')

    # Duplicate check — one result per student per semester
    existing = Result.query.filter_by(std_id=std_id, semester=semester).first()
    if existing:
        flash(f'A result for this student in semester {semester} already exists.', "error")
        return redirect(url_for('result.result'))

    new_result = Result(
        semester = semester,
        cgpa     = cgpa,
        std_id   = std_id
    )

    db.session.add(new_result)
    db.session.commit()
    log_action('Added', 'Result')

    flash(f'Result for semester {semester} has been added successfully.', "success")
    return redirect(url_for('result.result'))


# EDIT result
@result_bp.route('/admin/result/edit/<int:r_id>', methods=['GET', 'POST'])
def edit_result(r_id):
    denied = admin_required()
    if denied:
        return denied

    result      = Result.query.get_or_404(r_id)
    all_students = Student.query.all()

    if request.method == 'POST':
        result.semester = request.form.get('semester')
        result.cgpa     = request.form.get('cgpa')
        result.std_id   = request.form.get('std_id')

        db.session.commit()
        log_action('Updated', 'Result')
        flash(f'Result for semester {result.semester} has been updated successfully.', "success")
        return redirect(url_for('result.result'))

    return redirect(url_for('result.result'))


# DELETE result
@result_bp.route('/admin/result/delete/<int:r_id>', methods=['POST'])
def delete_result(r_id):
    denied = admin_required()
    if denied:
        return denied

    result   = Result.query.get_or_404(r_id)
    semester = result.semester

    db.session.delete(result)
    db.session.commit()
    log_action('Deleted', 'Result')

    flash(f'Result for semester {semester} has been permanently removed.', "error")
    return redirect(url_for('result.result'))