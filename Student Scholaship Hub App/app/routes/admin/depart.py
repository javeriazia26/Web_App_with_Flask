from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Department, University
from app.routes.admin.admin import admin_required, log_action  # shared helper
 
depart_bp = Blueprint('department', __name__)

# LIST all departments
@depart_bp.route('/admin/depart')
def depart():
    denied = admin_required()
    if denied:
        return denied
    
    all_deparemnts = Department.query.all()
    all_universities = University.query.all()
    
    edit_id = request.args.get('edit')
    editing_department = None
    if edit_id:
        editing_department = Department.query.get(edit_id) 
    
    return render_template('admin/depart.html',
        departments=all_deparemnts,
        universities=all_universities,
        editing_department=editing_department                
        )
    
# ── Add departments
@depart_bp.route('/admin/depart/add', methods=['POST'])
def add_depart():
    denied = admin_required()
    if denied:
        return denied
    
    d_name = request.form.get('d_name')
    c_name = request.form.get('c_name')
    uni_id = request.form.get('uni_id')
    
    new_depart = Department(
       d_name = d_name,
       c_name = c_name, 
       uni_id = uni_id
    )
    
    db.session.add(new_depart)
    db.session.commit()
    log_action('Added', 'Department') 

    flash(f'The "{d_name}" Department has been created successfully', "success")
    return redirect(url_for('department.depart')) 

#Edit Department
@depart_bp.route('/admin/depart/edit/<int:d_id>', methods=['GET', 'POST'])
def edit_depart(d_id):
    denied = admin_required()
    if denied:
        return denied
    
    department = Department.query.get_or_404(d_id)
    universities = University.query.all()
    
    if request.method == 'POST':
        department.d_name = request.form.get('d_name')
        department.c_name = request.form.get('c_name')
        department.uni_id = request.form.get('uni_id')
        
        db.session.commit()
        log_action('Updated', 'Department') 
        flash(f'The "{department.d_name}" Department has been updated successfully.', "success")
        return redirect(url_for('department.depart'))
    
    return redirect(url_for('department.depart'))

# ── Delete department
@depart_bp.route('/admin/depart/delete/<int:d_id>', methods=['POST'])
def delete_depart(d_id):
    denied = admin_required()
    if denied:
        return denied
 
    department = Department.query.get_or_404(d_id)
    department_name = department.d_name

    db.session.delete(department)
    db.session.commit()
    log_action('Deleted', 'Department')
 
    flash(f'The "{department_name}" Department has been permanently removed from the system.', "error")
    return redirect(url_for('department.depart'))