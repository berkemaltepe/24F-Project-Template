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
# Get student skills
@students.route('/student/<student_id>/skill/', methods=['GET'])
def get_student_skills(student_id):
    query = f'''
        SELECT ss.skill_id,
            ss.weight AS proficiency,
            s.skill_name,
            s.skill_type

        FROM Student_Skill ss
        JOIN Skill s ON ss.skill_id = s.skill_id
        WHERE student_id = {student_id}
    '''
    
    current_app.logger.info(f'GET /student/<student_id>/skill/ query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /student/<student_id>/skill/ Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get all skills
@students.route('/skills/', methods=['GET'])
def get_all_skills():
    query = f'''
        SELECT *
        FROM Skill;
    '''

    current_app.logger.info(f'GET /skills/ query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /skills/ Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add student skill
@students.route('/student/<student_id>/skill/', methods=['POST'])
def add_student_skill(student_id):
    the_data = request.json
    current_app.logger.info(the_data)

    skill_id = the_data['skill_id']
    proficiency = the_data['weight']

    query = f'''
        INSERT INTO Student_Skill
        VALUES({skill_id}, {student_id}, {proficiency});
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added student skill")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Update skill proficiency
@students.route('/student/<student_id>/skill/', methods=['PUT'])
def update_student_skill(student_id):
    the_data = request.json
    current_app.logger.info(the_data)

    skill_id = the_data['skill_id']
    proficiency = the_data['weight']

    query = f'''
        UPDATE Student_Skill
        SET weight = {proficiency}
        WHERE skill_id = {skill_id}
        AND student_id = {student_id};
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated student skill")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get all jobs
@students.route('/jobs/<student_id>/', methods=['GET'])
def get_all_jobs(student_id):
    query = f'''
        SELECT
            j.job_id,
            j.title AS job_title,
            j.description,
            j.location,
            j.pay_range,
            j.date_posted,
            j.status,
            e.name AS company,
            100.00 - ROUND(
            COALESCE(SUM(
                CASE
                    WHEN ss.weight IS NULL
                        THEN js.weight
                    WHEN ss.weight >= js.weight
                        THEN 0
                    ELSE
                        js.weight - ss.weight
                END
            ), 0) / COALESCE(SUM(js.weight), 1) * 100, 2
        ) AS match_percentage
        FROM Job AS j
        JOIN Employer AS e
            ON j.emp_id = e.emp_id
        LEFT JOIN Job_Skill AS js
            ON j.job_id = js.job_id
        LEFT JOIN Student_Skill AS ss
            ON js.skill_id = ss.skill_id
            AND ss.student_id = {student_id}
        GROUP BY
            j.job_id, e.name
        ORDER BY job_title ASC;
    '''

    current_app.logger.info(f'GET /jobs/<student_id>/ query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /jobs/<student_id>/ Result of query = {theData}')
    
    response = make_response(jsonify(theData))
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
            j.description,
            j.location,
            j.pay_range,
            j.date_posted,
            j.status,
            e.name AS company,
            100.00 - ROUND(
            COALESCE(SUM(
                CASE
                    WHEN ss.weight IS NULL
                        THEN js.weight
                    WHEN ss.weight >= js.weight
                        THEN 0
                    ELSE
                        js.weight - ss.weight
                END
            ), 0) / COALESCE(SUM(js.weight), 1) * 100, 2
        ) AS match_percentage
        FROM Job AS j
        JOIN Employer AS e
            ON j.emp_id = e.emp_id
        LEFT JOIN Job_Skill AS js
            ON j.job_id = js.job_id
        LEFT JOIN Student_Skill AS ss
            ON js.skill_id = ss.skill_id
            AND ss.student_id = {student_id}
        GROUP BY
            j.job_id, e.name
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
            100.00 - ROUND(
            COALESCE(SUM(
                CASE
                    WHEN ss.weight IS NULL
                        THEN js.weight
                    WHEN ss.weight >= js.weight
                        THEN 0
                    ELSE
                        js.weight - ss.weight
                END
            ), 0) / COALESCE(SUM(js.weight), 1) * 100, 2
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
            ss.weight AS student_proficiency,
            js.weight AS job_requirement,
            (ss.weight / js.weight) * 100 AS level_of_fit
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


