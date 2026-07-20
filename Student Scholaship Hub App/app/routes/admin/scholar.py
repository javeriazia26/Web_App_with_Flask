from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Scholarship, FundingSource
from app.routes.admin.admin import admin_required, log_action   # shared helper
from datetime import datetime
 
scholar_bp = Blueprint('scholarship', __name__)


# LIST all scholarships 
@scholar_bp.route('/admin/scholar')
def scholar():
    denied = admin_required()
    if denied:
        return denied
 
    all_scholarships = Scholarship.query.all()
    funding_sources  = FundingSource.query.all()
    
    edit_id = request.args.get('edit')
    editing_scholarship = None
    if edit_id:
        editing_scholarship = Scholarship.query.get(edit_id)
 
    return render_template('admin/scholar.html',
        scholarships=all_scholarships,
        funding_sources=funding_sources,
        editing_scholarship=editing_scholarship
    )
 
 
# ── Add Scholarship
@scholar_bp.route('/admin/scholar/add', methods=['POST'])
def add_scholar():
    denied = admin_required()
    if denied:
        return denied
 
    s_name       = request.form.get('s_name')
    total_amount = int(request.form.get('total_amount'))
    fund_type    = request.form.get('fund_type')
    start_date_str  = request.form.get('start_date')
    end_date_str     = request.form.get('end_date')
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date   = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    f_source_id  = int(request.form.get('f_source_id'))
    
 
    new_scholarship = Scholarship(
        s_name=s_name,
        total_amount=total_amount,
        fund_type=fund_type,
        start_date=start_date,
        end_date=end_date,
        f_source_id=f_source_id
    )
 
    db.session.add(new_scholarship)
    db.session.commit()
    log_action('Added', 'Scholarship')
 
    flash(f'The "{s_name}" scholarship has been created and is now active.', "success")
    return redirect(url_for('scholarship.scholar'))
 
 
# ── Edit Scholarship
@scholar_bp.route('/admin/scholar/edit/<int:s_id>', methods=['GET', 'POST'])
def edit_scholarship(s_id):
    denied = admin_required()
    if denied:
        return denied
 
    scholarship     = Scholarship.query.get_or_404(s_id)
    funding_sources = FundingSource.query.all()
 
    if request.method == 'POST':
        scholarship.s_name       = request.form.get('s_name')
        scholarship.total_amount = int(request.form.get('total_amount'))
        scholarship.fund_type    = request.form.get('fund_type')
        start_date_str = request.form.get('start_date')
        end_date_str   = request.form.get('end_date')
        scholarship.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        scholarship.end_date   = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        scholarship.f_source_id  = int(request.form.get('f_source_id'))

 
        db.session.commit()
        log_action('Updated', 'Scholarship')
        flash(f'The "{scholarship.s_name}" scholarship has been updated successfully.', "success")
        return redirect(url_for('scholarship.scholar'))
    
    return redirect(url_for('scholarship.scholar'))
 
 
# ── Delete Scholarship
@scholar_bp.route('/admin/scholar/delete/<int:s_id>',  methods=['POST'])
def delete_scholarship(s_id):
    denied = admin_required()
    if denied:
        return denied
 
    scholarship      = Scholarship.query.get_or_404(s_id)
    scholarship_name = scholarship.s_name

    db.session.delete(scholarship)
    db.session.commit()
    log_action('Deleted', 'Scholarship')
 
    flash(f'The "{scholarship_name}" scholarship has been permanently removed from the system.', "error")
    return redirect(url_for('scholarship.scholar'))