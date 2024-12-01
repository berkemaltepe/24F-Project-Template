from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Blueprint for advisor routes
advisors = Blueprint('advisors', __name__)

# ------------------------------------------------------------
# Route: Get advisor information
@advisors.route('/advisor/<int:advisor_id>', methods=['GET'])  # Ensure advisor_id is an integer
def get_advisor_info(advisor_id):
    """
    Endpoint to get advisor information.
    """
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        # Use a parameterized query to prevent SQL injection
        query = '''
            SELECT name, advisor_id, email, department
            FROM Advisor
            WHERE advisor_id = %s
        '''
        cursor.execute(query, (advisor_id,))  # Pass advisor_id as a parameter safely

        # Fetch the results
        advisor = cursor.fetchall()  # Use fetchone if only one record is expected

        # Check if the advisor exists
        if not advisor:
            return jsonify({"error": "Advisor not found"}), 404

        # Return the results as JSON
        return make_response(jsonify(advisor), 200)
    except Exception as e:
        current_app.logger.error(f"Error fetching advisor info: {e}")
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------
# Route: Update advisor email
@advisors.route('/advisor/<int:advisor_id>/email', methods=['PUT'])
def update_advisor_email(advisor_id):
    """
    Endpoint to update advisor email.
    """
    try:
        # Log the PUT request
        current_app.logger.info('PUT /advisor/email route')

        # Parse the request body for new email data
        advisor_info = request.json
        new_email = advisor_info.get('email')

        if not new_email:
            return jsonify({"error": "Email field is required."}), 400

        # Update the advisor's email in the database
        query = 'UPDATE Advisor SET email = %s WHERE advisor_id = %s'
        data = (new_email, advisor_id)
        cursor = db.get_db().cursor()
        cursor.execute(query, data)
        db.get_db().commit()

        return jsonify({"message": "Advisor email updated successfully!"}), 200
    except Exception as e:
        current_app.logger.error(f"Error updating advisor email: {e}")
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------
# Route: Get list of students assigned to a specific advisor
@advisors.route('/advisor/<advisor_id>/list-of-students', methods=['GET'])
def get_students_by_advisor(advisor_id):
    # SQL query to fetch students
    query = f'''
        SELECT
            s.student_id,
            s.name,
            s.email,
            s.location,
            s.major,
            s.coop_status,
            s.resume,
            s.level,
            s.linkedin_profile,
            s.gpa,
            a.name AS advisor_name
        FROM Student AS s
        JOIN Advisor AS a ON s.advisor_id = a.advisor_id
        WHERE a.advisor_id = {advisor_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    students = cursor.fetchall()
    # Return as JSON response
    return make_response(jsonify(students), 200)

# ------------------------------------------------------------
# Route: Get all active job postings
@advisors.route('/advisor/employer/', methods=['GET'])
def get_all_job_postings():
    # SQL query to fetch all active job postings
    query = '''
        SELECT 
            j.job_id,
            j.title AS job_title,
            e.name AS employer_name,
            j.location,
            j.pay_range,
            j.status,
            j.date_posted
        FROM Job AS j
        JOIN Employer AS e ON j.emp_id = e.emp_id
        WHERE j.status = 'Open'
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    jobs = cursor.fetchall()
    return make_response(jsonify(jobs), 200)

# ------------------------------------------------------------
# Route: Compare a student's skills to a specific job's requirements
@advisors.route('/advisor/job/<int:job_id>/skills/compare/<int:student_id>', methods=['GET'])
def compare_student_to_job_skills(job_id, student_id):
    # SQL query to compare student skills with job requirements
    query = f'''
        SELECT
            sk.skill_name,
            ss.weight AS student_proficiency,
            js.weight AS job_requirement,
            ROUND(
                COALESCE(SUM(
                    CASE
                        WHEN ss.weight IS NULL THEN js.weight
                        WHEN ss.weight >= js.weight THEN 0
                        ELSE js.weight - ss.weight
                    END
                ), 0) / COALESCE(SUM(js.weight), 1) * 100, 2
            ) AS total_skill_gap
        FROM Student_Skill AS ss
        JOIN Skill AS sk ON ss.skill_id = sk.skill_id
        LEFT JOIN Job_Skill AS js ON sk.skill_id = js.skill_id
        WHERE ss.student_id = {student_id} AND js.job_id = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    comparison = cursor.fetchall()
    return make_response(jsonify(comparison), 200)

# ------------------------------------------------------------
# Route: Fetch detailed job information including required skills
@advisors.route('/advisor/job/<int:job_id>/details', methods=['GET'])
def get_job_details_with_skills(job_id):
    # SQL query to fetch job details and required skills
    query = f'''
        SELECT
            j.job_id,
            j.title AS job_title,
            j.description,
            j.location,
            j.pay_range,
            sk.skill_name,
            js.weight AS required_proficiency
        FROM Job AS j
        JOIN Job_Skill AS js ON j.job_id = js.job_id
        JOIN Skill AS sk ON js.skill_id = sk.skill_id
        WHERE j.job_id = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    details = cursor.fetchall()
    return make_response(jsonify(details), 200)

# ------------------------------------------------------------
# Route: Assign a student to an advisor (PUT) or remove a student (DELETE)
@advisors.route('/advisor/<int:advisor_id>/student/<int:student_id>', methods=['PUT', 'DELETE'])
def modify_advisor_students(advisor_id, student_id):
    if request.method == 'PUT':
        # Assign student to advisor
        query = f'''
            UPDATE Student
            SET advisor_id = {advisor_id}
            WHERE student_id = {student_id}
        '''
        action = 'added to'
    elif request.method == 'DELETE':
        # Remove student from advisor
        query = f'''
            UPDATE Student
            SET advisor_id = NULL
            WHERE student_id = {student_id}
        '''
        action = 'removed from'

    # Execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response(f"Student successfully {action} advisor's list.", 200)

# ------------------------------------------------------------
# Route: Calculate match percentage between a student and a job
@advisors.route('/advisor/job/<int:job_id>/match/<int:student_id>', methods=['GET'])
def calculate_match_percentage(job_id, student_id):
    # SQL query to calculate match percentage
    query = f'''
        SELECT
            j.job_id,
            j.title AS job_title,
            s.student_id,
            s.name AS student_name,
            ROUND(
                (SUM(CASE
                    WHEN ss.skill_id = js.skill_id THEN 1
                    ELSE 0
                END) / COUNT(js.skill_id)) * 100, 2
            ) AS match_percentage
        FROM Job AS j
        JOIN Job_Skill AS js ON j.job_id = js.job_id
        JOIN Student_Skill AS ss ON js.skill_id = ss.skill_id
        JOIN Student AS s ON ss.student_id = s.student_id
        WHERE s.student_id = {student_id} AND j.job_id = {job_id}
        GROUP BY j.job_id, s.student_id
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    match = cursor.fetchone()
    return make_response(jsonify(match), 200)

# SUMMARY
# |Route|	                                       |Method|	 |Purpose|
# /advisor/<advisor_id>/list-of-students	        GET	      Fetch students assigned to an advisor.
# /advisor/employer/	                            GET	      Fetch all active job postings.
# /advisor/job/<job_id>/skills/compare/<student_id>	GET	      Compare a student's skills to a job.
# /advisor/job/<job_id>/details	                    GET	      Fetch detailed job and skill information.
# /advisor/<advisor_id>/student/<student_id>	    PUT	      Assign a student to an advisor.
# /advisor/<advisor_id>/student/<student_id>	    DELETE	  Remove a student from an advisor.
# /advisor/job/<job_id>/match/<student_id>	        GET	      Calculate match percentage.
