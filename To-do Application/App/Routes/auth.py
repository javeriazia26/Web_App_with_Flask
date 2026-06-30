# Authorization routes
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db 
from app.models import Credential
from app.routes.reg_form import RegistrationForm
from app.routes.log_form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__) #creating object for blueprint


# Registration Route
@auth_bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():       
    #it will return true when form submitted successfully
        username = request.form['username'] 
        password = request.form['password']
        hashed_password = generate_password_hash(password) 

        #check if user exists or not
        existing_user = Credential.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists", "info")
            return redirect(url_for('auth.register'))
        
        #adding new user
        user = Credential(username=username, hashed_password=hashed_password)
        db.session.add(user)  # Add the new user to the session
        db.session.commit()  # Commit the session to save the user to the database
        
        # log the user in by saving username in session so tasks view can be accessed
        session["user_id"] = user.id
        flash("Registered successfully", 'success')
        return redirect(url_for('tasks.view_tasks'))
    return render_template('register.html', form=form)    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        user = Credential.query.filter_by(username=username).first()
        if user and check_password_hash(user.hashed_password, password):
            session['user_id'] = user.id   
            flash('Login successful!', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Login Failed', 'failure')
            flash('Invalid Username or Password', 'failure')

    return render_template('login.html', form=form)

@auth_bp.route('/logout') 
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('auth.register'))
