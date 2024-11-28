from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a blueprint for employer routes
employer_routes = Blueprint('employer_routes', __name__)

@employer_routes.route('/employer/<emp_id>', methods=['GET'])
def get_emp_info(emp_id):
    """
    Endpoint to get a list of students.
    """
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        # Query the database for students
        cursor.execute("SELECT name, emp_id, industry, email FROM Employer WHERE emp_id = {0}".format(emp_id))
        emp = cursor.fetchall()

        # Convert the result to a list of dictionaries
        
        return make_response(jsonify(emp)), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching emp info: {e}")
        return jsonify({"error": str(e)}), 500

@employer_routes.route('/employers/<emp_id>/email', methods=['PUT'])
def update_employer_email(emp_id):
    current_app.logger.info('PUT /employers route')
    emp_info = request.json
    emp_id = emp_info['id']
    email = emp_info['email']

    query = 'UPDATE Employer SET email = %s WHERE emp_id = %s'
    data = (email, emp_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'email updated!'

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

@employer_routes.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """
    Endpoint to get a list of students.
    """
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        # Query the database for students
        cursor.execute("SELECT student_id, name, major FROM Student WHERE student_id = {0};".format(student_id))
        student = cursor.fetchall()

        # Convert the result to a list of dictionaries
        
        return make_response(jsonify(student)), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching students: {e}")
        return jsonify({"error": str(e)}), 500


@employer_routes.route('/students/<student_id>/skills', methods=['GET'])
def get_student_skills(student_id):
    """
    Endpoint to fetch a student's skills and weights.
    """
    try:
        # Database query to fetch the student's skills
        cursor = db.get_db().cursor()

        query = """
        SELECT sk.skill_name, ss.weight
        FROM Student_Skill AS ss
        JOIN Skill AS sk ON ss.skill_id = sk.skill_id
        WHERE ss.student_id = {0};
        """.format(student_id)

        cursor.execute(query)
        # Transform query results into JSON response
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@employer_routes.route('/jobs/<job_id>/skills', methods=['GET'])
def get_job_skills(job_id):
    """
    Endpoint to fetch required skills for a specific job.
    """
    try:
        cursor = db.get_db().cursor()
        # Database query to fetch job-required skills
        query = """
        SELECT sk.skill_name, js.weight
        FROM Job_Skill AS js
        JOIN Skill AS sk ON js.skill_id = sk.skill_id
        WHERE js.job_id = {0};
        """.format(job_id)
        cursor.execute(query)
        # Transform query results into JSON response
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employer_routes.route('/employers/<int:emp_id>/jobs', methods=['GET'])
def get_jobs(emp_id):
    """
    Endpoint to fetch jobs for a specific employer.
    """
    try:
        cursor = db.get_db().cursor()
        # Database query to fetch jobs for the employer
        query = """
        SELECT j.job_id, j.title
        FROM Job AS j
        JOIN Employer AS e ON j.emp_id = e.emp_id
        WHERE e.emp_id = {0};
        """.format(emp_id)
        cursor.execute(query)
        # Transform query results into JSON response
        results = cursor.fetchall()
        return make_response(jsonify(results)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ensure to register this blueprint in your main application (e.g., backend_app.py)
# @employer_routes.route('/job/<job_id>/student_matches', methods=['GET'])
# def get_matches(job_id):
#     try:
#         cursor = db.get_db().cursor()
#         query = """
#         SELECT
#         s.student_id,
#         s.name AS student_name,
#         j.job_id,
#         j.title AS job_title,
#         ROUND(
#             SUM(
#                 CASE
#                     WHEN ss.weight IS NULL
#                         THEN js.weight
#                     WHEN ss.weight >= js.weight
#                         THEN 0
#                     ELSE
#                         js.weight - ss.weight
#                 END
#             ) / SUM(js.weight) * 100, 2
#         ) AS total_skill_gap
#         FROM Student AS s
#         CROSS JOIN Job AS j
#         JOIN Job_Skill AS js ON js.job_id = j.job_id
#         LEFT JOIN Student_Skill AS ss ON s.student_id = ss.student_id AND ss.skill_id = js.skill_id
#         WHERE j.job_id = 3
#         GROUP BY s.student_id, j.job_id;
#         """
        
#         cursor.execute(query)