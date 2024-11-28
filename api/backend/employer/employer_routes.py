from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a blueprint for employer routes
employer_routes = Blueprint('employer_routes', __name__)

# Sample data: List of students

@employer_routes.route('/students', methods=['GET'])
def get_students():
    """
    Endpoint to get a list of students.
    """
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        # Query the database for students
        cursor.execute("SELECT student_id, name, major FROM Student;")
        students = cursor.fetchall()

        # Convert the result to a list of dictionaries
        
        return make_response(jsonify(students)), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching students: {e}")
        return jsonify({"error": str(e)}), 500

# Ensure to register this blueprint in your main application (e.g., backend_app.py)
