
############################################################
# PERSONA: STUDENT
# This file goes over the routes required for students
############################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

students = Blueprint('students', __name__)

#------------------------------------------------------------
# Calculate skill gap of student for job
@students.route('/<student_id>/job/<job_id>', methods=['GET'])
def get_skill_gap(student_id, job_id):
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
        JOIN Job_Skill AS js
            ON j.job_id = js.job_id
        JOIN Student_Skill AS ss
            ON js.skill_id = ss.skill_id
        JOIN Student s
            ON ss.student_id = s.student_id
        WHERE
            s.student_id = {student_id}
            and j.job_id = {job_id}
        GROUP BY
            j.job_id, s.student_id;
    '''

    current_app.logger.info(f'GET /<student_id>/job/<job_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /<student_id>/job/<job_id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Compare student skills to job skills
@students.route('/<student_id>/job/<job_id>/skills', methods=['GET'])
def get_job_skill_comparison(student_id, job_id):
    query = f'''
        SELECT
            sk.skill_id,
            sk.skill_name,
            ss.proficiency AS student_proficiency,
            js.weight AS job_requirement,
            js.min_proficiency AS job_min_proficiency,
            (ss.proficiency / js.min_proficiency) * js.weight AS level_of_fit
        FROM Student_Skill AS ss
        JOIN Skill AS sk ON ss.skill_id = sk.skill_id
        LEFT JOIN Job_Skill AS js ON sk.skill_id = js.skill_id
        WHERE
            ss.student_id = {student_id}
            and js.job_id = {job_id};
    '''

    current_app.logger.info(f'GET /<student_id>/job/<job_id>/skill query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /<student_id>/job/<job_id>/skill Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get student information
@students.route('/student/<student_id>/', methods=['GET'])
def get_student(student_id):
    query = f'''
        SELECT *
        FROM Student
        WHERE student_id = {student_id};
    '''

    current_app.logger.info(f'GET /student/<student_id>/ query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /student/<student_id>/ Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Update student profile
@students.route('/student/<student_id>/', methods=['PUT'])
def update_student(student_id):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    email = the_data['email']
    location = the_data['location']
    major = the_data['major']
    coop_status = the_data['coop_status']
    resume = the_data['resume']
    level = the_data['level']
    linkedin_profile = the_data['linkedin_profile']
    gpa = the_data['gpa']
    
    query = f'''
        UPDATE Student
        SET name = '{name}',
            email = '{email}',
            location = '{location}',
            major = '{major}',
            coop_status = '{coop_status}',
            resume = '{resume}',
            level = '{level}',
            linkedin_profile = '{linkedin_profile}',
            gpa = {gpa}
        WHERE student_id = {student_id};
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated product")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get jobs by best match to student
@students.route('/job/best_match/<student_id>/', methods=['GET'])
def get_best_jobs(student_id):
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
        JOIN Job_Skill AS js
            ON j.job_id = js.job_id
        JOIN Student_Skill AS ss
            ON js.skill_id = ss.skill_id
        JOIN Student s
            ON ss.student_id = s.student_id
        WHERE
            s.student_id = 2 -- Replace with specific student ID
        GROUP BY
            j.job_id
        ORDER BY match_percentage DESC;
    '''

    current_app.logger.info(f'GET /job/best_match/<student_id>/ query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /job/best_match/<student_id>/ Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


