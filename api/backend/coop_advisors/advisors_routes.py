
########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
advisors = Blueprint('advisors', __name__)

#------------------------------------------------------------
# Get all students from the database
@advisors.route('/students/', methods=['GET'])
def get_students():
    # get all students
    query = '''
        SELECT *
        FROM Students
       '''
    # cursor object from the database
    cursor.get_db().cursor()
    # use cursor to exectute query
    cursor.execute(query)
    # fetch all the data from the cursor
    theData = cursor.fetchall()
    # create a HTTP Response object and add results of the query to it
    response = make_response(jsonify(theData))
    # send the response back
    return response

#------------------------------------------------------------
# Add new students to the database
@advisors.route('/students/', methods=['POST'])
def get_students():
    # get the request JSON data
    theData = request.json
    # extract student details from the JSON payload
    name = theData.get('name')
    age = theData.get('age')
    # query to insert a new student record
    query = f'''
        INSERT INTO students (name, age) 
        VALUES ('{name}', {age})
    '''
    # execute the query and commit the changes to the database
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    # return a success message with a 201 HTTP status code
    return make_response("Student added successfully.", 201)

#------------------------------------------------------------
# Remove a student from the database
@advisors.route('/student/', methods=['DELETE'])
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
# View a student's profile
@advisors.route('/student/<int:student_id>', methods=['GET'])
def get_student_profile(student_id):
    # SQL query to fetch a student record by ID
    query = f'''
        SELECT * 
        FROM students 
        WHERE id = {student_id}
    '''
    # execute the query and commit the changes to the database
    cursor = db.get_db().cursor()
    cursor.execute(query)
    student = cursor.fetchone()
    # return the result as JSON with a 200 HTTP status code
    return make_response(jsonify(student), 200)

#------------------------------------------------------------
# View a student's skills
@advisors.route('/student/<int:student_id>/skills', methods=['GET'])
def get_student_skills(student_id):
    # SQL query to fetch skills for a specific student
    query = f'''
        SELECT skills.name 
        FROM student_skills 
        JOIN skills ON student_skills.skill_id = skills.id 
        WHERE student_skills.student_id = {student_id}
    '''
    # execute the query and fetch the results
    cursor = db.get_db().cursor()
    cursor.execute(query)
    skills = cursor.fetchall()
    # return the results as JSON with a 200 HTTP status code
    return make_response(jsonify(skills), 200)

#------------------------------------------------------------
# Get all employers
@advisors.route('/employer/', methods=['GET'])
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
# View a job posting
@advisors.route('/job/<int:job_id>', methods=['GET'])
def get_job_posting(job_id):
    # SQL query to fetch a job record by ID
    query = f'''
        SELECT * 
        FROM jobs 
        WHERE id = {job_id}
    '''
    # execute the query and fetch the result