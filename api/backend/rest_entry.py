from flask import Flask

from backend.db_connection import db

from backend.employer.employer_routes import employer_routes
from backend.depthead.dept_head_routes import depthead_routes
from backend.system_admin.system_admin_routes import system_admin_routes
from backend.students.students_routes import students
from backend.coop_advisor.advisors_routes import advisors
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    # IGNORE TILL HERE !!!!!!!!!!!!!!!!

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(employer_routes, url_prefix="/employer")
    app.register_blueprint(depthead_routes, url_prefix="/depthead")
    app.register_blueprint(system_admin_routes, url_prefix='/system_admin')
    app.register_blueprint(students,    url_prefix='/s')
    app.register_blueprint(advisors, url_prefix="/a")

    # Don't forget to return the app object
    return app

