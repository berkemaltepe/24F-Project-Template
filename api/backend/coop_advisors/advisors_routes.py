
############################################################
# PERSONA: CO-OP ADVISOR
# This file goes over the routes required for co-op advisors
############################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Blueprint for NUSkillMatch
nu_skillmatch = Blueprint('nu_skillmatch', __name__)

#------------------------------------------------------------
# Get all students from the database
@nu_skillmatch.route('/students/', methods=['GET'])
def get_students():
    # get all students
    query = '''
        SELECT *
        FROM Students
       '''
    # cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to exectute query
    cursor.execute(query)
    # fetch all the data from the cursor
    students = cursor.fetchall()
    # create a HTTP Response object and add results of the query to it
    response = make_response(jsonify(students), 200)
    # send the response back
    return response

#------------------------------------------------------------
# Add new students to the database
@nu_skillmatch.route('/students/', methods=['POST'])
def add_students():
    # get the request JSON data
    data = request.json
    # extract student details from the JSON payload
    name = data.get('name')
    email = data.get('email')
    location = data.get('location')
    major = data.get('major')
    gpa = data.get('gpa')
    linkedin_profile = data.get('linkedin_profile')
    # query to insert a new student record
    query = f"""
        INSERT INTO Student (name, email, location, major, gpa, linkedin_profile)
        VALUES ('{name}', '{email}', '{location}', '{major}', {gpa}, '{linkedin_profile}')
    """
    # execute the query and commit the changes to the database
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    # return a success message with a 201 HTTP status code
    return make_response("Student added successfully.", 201)

#------------------------------------------------------------
# Remove a student from the database
@nu_skillmatch.route('/student/', methods=['DELETE'])
def delete_student():
    # get the request JSON data
    data = request.json
    # extract the student ID from the JSON payload
    student_id = data.get('student_id')
    # SQL query to delete a student record by ID
    query = f'''
        DELETE FROM students 
        WHERE id = {student_id}
    '''
    # execute the query and commit the changes to the database
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    # return a success message with a 200 HTTP status code
    return make_response("Student removed successfully.", 200)

#------------------------------------------------------------
# View student profile
@nu_skillmatch.route('/student/<int:student_id>', methods=['GET'])
def get_student_profile(student_id):
    # SQL query to fetch a student profile by ID
    query = f'''
        SELECT * 
        FROM Student 
        WHERE student_id = {student_id}
    '''
    # Execute query and fetch the result
    cursor = db.get_db().cursor()
    cursor.execute(query)
    student = cursor.fetchone()
    # Return the student profile as JSON with a 200 HTTP status
    return make_response(jsonify(student), 200)

#------------------------------------------------------------
# View a student's skills
@nu_skillmatch.route('/student/<int:student_id>/skills', methods=['GET'])
def get_student_skills(student_id):
    # SQL query to fetch skills for a specific student
    query = f'''
        SELECT Skill.skill_name, Student_Skill.proficiency
        FROM Student_Skill
        JOIN Skill ON Student_Skill.skill_id = Skill.skill_id
        WHERE Student_Skill.student_id = {student_id}
    '''
    # execute the query and fetch the results
    cursor = db.get_db().cursor()
    cursor.execute(query)
    skills = cursor.fetchall()
    # return the results as JSON with a 200 HTTP status code
    return make_response(jsonify(skills), 200)

#------------------------------------------------------------
# Get all employers
@nu_skillmatch.route('/employer/', methods=['GET'])
def get_employers():
    # SQL query to fetch all employers
    query = '''
        SELECT * 
        FROM employers
    '''
    # execute the query and fetch the results
    cursor = db.get_db().cursor()
    cursor.execute(query)
    employers = cursor.fetchall()
    # return the results as JSON with a 200 HTTP status code
    return make_response(jsonify(employers), 200)

#------------------------------------------------------------
# View a job posting details
@nu_skillmatch.route('/job/<int:job_id>', methods=['GET'])
def get_job_posting(job_id):
    # SQL query to fetch a job record by ID
    query = f'''
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
    # execute the query and fetch the result
    cursor = db.get_db().cursor()
    cursor.execute(query)
    job = cursor.fetchone()
    # return the result as JSON with a 200 HTTP status code
    return make_response(jsonify(job), 200)

#------------------------------------------------------------
# Calculate match percentage
@nu_skillmatch.route('/job/<int:job_id>/match/<int:student_id>', methods=['GET'])
def calculate_match(job_id, student_id):
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
        JOIN Student s ON ss.student_id = s.student_id
        WHERE
            s.student_id = {student_id}
            AND j.job_id = {job_id}
        GROUP BY j.job_id, s.student_id
    '''
    # execute query and fetch the result
    cursor = db.get_db().cursor()
    cursor.execute(query)
    match = cursor.fetchone()
    # return the match percentage as JSON with a 200 HTTP status
    return make_response(jsonify(match), 200)

#------------------------------------------------------------
# Retrieve detailed information about a job, including required skills
@nu_skillmatch.route('/job/<int:job_id>/details', methods=['GET'])
def get_job_details_with_skills(job_id):
    query = f'''
        SELECT
            j.job_id,
            j.title AS job_title,
            j.description,
            j.location,
            j.pay_range,
            sk.skill_name,
            js.min_proficiency AS required_proficiency,
            js.weight AS skill_importance
        FROM Job AS j
        JOIN Job_Skill AS js ON j.job_id = js.job_id
        JOIN Skill AS sk ON js.skill_id = sk.skill_id
        WHERE j.job_id = {job_id}
    '''
    # execute query and fetch the result
    cursor = db.get_db().cursor()
    cursor.execute(query)
    details = cursor.fetchall()
    # return the result as JSON with a 200 HTTP status code
    return make_response(jsonify(details), 200)

# Retrieve a student's skills and their proficiency levels
@nu_skillmatch.route('/student/<int:student_id>/skills', methods=['GET'])
def get_student_skills_and_proficiency(student_id):
    query = f'''
        SELECT
            s.student_id,
            s.name AS student_name,
            sk.skill_name,
            ss.proficiency
        FROM Student AS s
        JOIN Student_Skill AS ss ON s.student_id = ss.student_id
        JOIN Skill AS sk ON ss.skill_id = sk.skill_id
        WHERE s.student_id = {student_id}
    '''
    # execute query and fetch the result
    cursor = db.get_db().cursor()
    cursor.execute(query)
    skills = cursor.fetchall()
    # return the result as JSON with a 200 HTTP status code
    return make_response(jsonify(skills), 200)

# Compare a student's skills to the requirements of a specific job.
@nu_skillmatch.route('/job/<int:job_id>/skills/compare/<int:student_id>', methods=['GET'])
def compare_student_to_job_skills(job_id, student_id):
    query = f'''
        SELECT
            sk.skill_id,
            sk.skill_name,
            ss.proficiency AS student_proficiency,
            js.weight AS job_requirement,
            (ss.proficiency / js.min_proficiency) * js.weight AS level_of_fit
        FROM Student_Skill AS ss
        JOIN Skill AS sk ON ss.skill_id = sk.skill_id
        LEFT JOIN Job_Skill AS js ON sk.skill_id = js.skill_id
        WHERE ss.student_id = {student_id} AND js.job_id = {job_id}
    '''