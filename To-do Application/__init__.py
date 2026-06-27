from flask import Flask, redirect, url_for

#we're calling main flask class so we can create an instance of it in the create_app function
from flask_sqlalchemy import SQLAlchemy
#we call the flask_sqlalchemy class so we can create an instance of it in the create_app function and use it to connect to our database and perform operations on it

#create database connection object globally
db = SQLAlchemy() #object created for database connection

def create_app():  #this will create app
    app = Flask(__name__) #this will create object

    #we set secret key so we can use it for session management and other security-related features in our Flask application
    app.config['SECRET_KEY'] = 'your-secret-key'
    # Configure the database URI (replace with your actual database URI)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    # Disable SQLAlchemy event system to save resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database connection with the Flask app
    db.init_app(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    #
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app