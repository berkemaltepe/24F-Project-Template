
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
        SELECT Job.title, Job.description, Job.location, Job.pay_range, Skill.skill_name, Job_Skill.min_proficiency
        FROM Job
        JOIN Job_Skill ON Job.job_id = Job_Skill.job_id
        JOIN Skill ON Job_Skill.skill_id = Skill.skill_id
        WHERE Job.job_id = {job_id}
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
            ROUND(
                (SUM(CASE WHEN Student_Skill.skill_id = Job_Skill.skill_id THEN 1 ELSE 0 END) 
                / COUNT(Job_Skill.skill_id)) * 100, 2
            ) AS match_percentage
        FROM Job_Skill
        LEFT JOIN Student_Skill ON Job_Skill.skill_id = Student_Skill.skill_id
        WHERE Job_Skill.job_id = {job_id} AND Student_Skill.student_id = {student_id}
    '''
    # Execute query and fetch the result
    cursor = db.get_db().cursor()
    cursor.execute(query)