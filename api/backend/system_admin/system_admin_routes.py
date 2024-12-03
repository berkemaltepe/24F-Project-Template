from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a blueprint for system admin routes
system_admin_routes = Blueprint('system_admin_routes', __name__)

#------------------------------------------------------------
# Gets the info of all jobs in the system
@system_admin_routes.route('/job', methods=['GET'])
def get_all_jobs():
    query = '''
        SELECT *
        FROM Job
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    job_data = cursor.fetchall()
    return make_response(jsonify(job_data)), 200
    
#------------------------------------------------------------
# Adds a new job to the system
@system_admin_routes.route('/job', methods=['POST'])
def add_job():
    job_data = request.json
    id = job_data['job_id']
    title = job_data['title']
    emp_id = job_data['emp_id']
    desc = job_data['description']
    loc = job_data['location']
    pay = job_data['pay_range']
    status = job_data['status']

    query = f'''
        INSERT INTO Job (job_id, title, emp_id, description, location, pay_range, status)
        VALUES ({id}, '{title}', {emp_id}, '{desc}', '{loc}', '{pay}', '{status}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added job")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of a given job from its job_id
@system_admin_routes.route('/job/<job_id>', methods=['GET'])
def get_job_info(job_id):
    query = f'''
        SELECT job_id, title, emp_id, description, location, pay_range, status
        FROM Job
        WHERE job_id = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    job_data = cursor.fetchall()
    response = make_response(jsonify(job_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Removes a job from the system
@system_admin_routes.route('/job/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    query = f'''
    DELETE FROM Job
    WHERE job_id = {job_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted job")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of all skills in the system
@system_admin_routes.route('/skill', methods=['GET'])
def get_all_skills():
    query = '''
        SELECT *
        FROM Skill
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    skill_data = cursor.fetchall()
    return make_response(jsonify(skill_data)), 200

#------------------------------------------------------------
# Adds a new skill to the system
@system_admin_routes.route('/skill', methods=['POST'])
def add_skill():
    skill_data = request.json

    id = skill_data['skill_id']
    name = skill_data['skill_name']
    type = skill_data['skill_type']
    weight = skill_data['weight']
    
    query = f'''
        INSERT INTO Skill (skill_id, skill_name, skill_type, weight)
        VALUES ({id}, '{name}', '{type}', {weight})
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added skill")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of a given skill from its skill_id
@system_admin_routes.route('/skill/<skill_id>', methods=['GET'])
def get_skill_info(skill_id):
    query = f'''
        SELECT skill_id, skill_name, skill_type, weight
        FROM Skill
        WHERE skill_id = {skill_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    skill_data = cursor.fetchall()
    response = make_response(jsonify(skill_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Removes a skill from the system
@system_admin_routes.route('/skill/<skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    query = f'''
    DELETE FROM Skill
    WHERE skill_id = {skill_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted skill")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of all employers in the system
@system_admin_routes.route('/employer', methods=['GET'])
def get_all_employers():
    query = '''
        SELECT *
        FROM Employer
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    emp_data = cursor.fetchall()
    return make_response(jsonify(emp_data)), 200

#------------------------------------------------------------
# Adds a new employer to the system
@system_admin_routes.route('/employer', methods=['POST'])
def add_employer():
    employer_data = request.json

    id = employer_data['emp_id']
    admin_id = employer_data['admin_id']
    name = employer_data['name']
    email = employer_data['email']
    industry = employer_data['industry']
    num_apps = employer_data['num_applications']
    
    query = f'''
        INSERT INTO Employer (emp_id, admin_id, name, email, industry, num_applications)
        VALUES ({id}, {admin_id}, '{name}', '{email}', '{industry}', {num_apps})
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added employer")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of a given employer from its emp_id
@system_admin_routes.route('/employer/<emp_id>', methods=['GET'])
def get_employer_info(emp_id):
    query = f'''
        SELECT emp_id, admin_id, name, email, industry, num_applications
        FROM Employer
        WHERE emp_id = {emp_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    employer_data = cursor.fetchall()
    response = make_response(jsonify(employer_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Removes a employer from the system
@system_admin_routes.route('/employer/<emp_id>', methods=['DELETE'])
def delete_employer(emp_id):
    query = f'''
    DELETE FROM Employer
    WHERE emp_id = {emp_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted employer")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of all advisors in the system
@system_admin_routes.route('/advisor', methods=['GET'])
def get_all_advisors():
    query = '''
        SELECT *
        FROM Advisor
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    advisor_data = cursor.fetchall()
    return make_response(jsonify(advisor_data)), 200

#------------------------------------------------------------
# Adds a new advisor to the system
@system_admin_routes.route('/advisor', methods=['POST'])
def add_advisor():
    advisor_data = request.json

    id = advisor_data['advisor_id']
    admin_id = advisor_data['admin_id']
    name = advisor_data['name']
    email = advisor_data['email']
    department = advisor_data['department']
    
    query = f'''
        INSERT INTO Advisor (advisor_id, admin_id, name, email, department)
        VALUES ({id}, {admin_id}, '{name}', '{email}', '{department}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added advisor")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of a given advisor from its advisor_id
@system_admin_routes.route('/advisor/<advisor_id>', methods=['GET'])
def get_advisor_info(advisor_id):
    query = f'''
        SELECT advisor_id, admin_id, name, email, department
        FROM Advisor
        WHERE advisor_id = {advisor_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    advisor_data = cursor.fetchall()
    response = make_response(jsonify(advisor_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Removes a advisor from the system
@system_admin_routes.route('/advisor/<advisor_id>', methods=['DELETE'])
def delete_advisor(advisor_id):
    query = f'''
    DELETE FROM Advisor
    WHERE advisor_id = {advisor_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted advisor")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of all students in the system
@system_admin_routes.route('/student', methods=['GET'])
def get_all_students():
    query = '''
        SELECT student_id, name, email, location, major, coop_status, resume, level,
                    linkedin_profile, gpa, advisor_id, admin_id
        FROM Student
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    students_data = cursor.fetchall()
    return make_response(jsonify(students_data)), 200

#------------------------------------------------------------
# Adds a new student to the system
@system_admin_routes.route('/student', methods=['POST'])
def add_student():
    student_data = request.json
    id = student_data['student_id']
    name = student_data['name']
    email = student_data['email']
    loc = student_data['location']
    major = student_data['major']
    status = student_data['coop_status']
    resume = student_data['resume']
    level = student_data['level']
    linkedin = student_data['linkedin_profile']
    gpa = student_data['gpa']
    advisor_id = student_data['advisor_id']
    admin_id = student_data['admin_id']
    
    query = f'''
        INSERT INTO Student (student_id, name, email, location, major, coop_status, resume, level,
                    linkedin_profile, gpa, advisor_id, admin_id)

        VALUES ({id}, '{name}', '{email}', '{loc}', '{major}', '{status}', '{resume}', '{level}',
        '{linkedin}', {gpa}, {advisor_id}, {admin_id})
        '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added student")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of a given student from its student_id
@system_admin_routes.route('/student/<student_id>', methods=['GET'])
def get_student_info(student_id):
    query = f'''
        SELECT student_id, name, email, location, major, coop_status, resume, level,
                    linkedin_profile, gpa, advisor_id, admin_id
        FROM Student
        WHERE student_id = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    student_data = cursor.fetchall()
    response = make_response(jsonify(student_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Removes a student from the system
@system_admin_routes.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    query = f'''
    DELETE FROM Student
    WHERE student_id = {student_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted student")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of all faculties in the system
@system_admin_routes.route('/faculty', methods=['GET'])
def get_all_faculties():
    query = '''
        SELECT *
        FROM Dpt_Faculty
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    faculty_data = cursor.fetchall()
    return make_response(jsonify(faculty_data)), 200

#------------------------------------------------------------
# Adds a new faculty to the system
@system_admin_routes.route('/faculty', methods=['POST'])
def add_faculty():
    faculty_data = request.json

    id = faculty_data['faculty_id']
    admin_id = faculty_data['admin_id']
    name = faculty_data['name']
    email = faculty_data['email']
    department = faculty_data['department']
    
    query = f'''
        INSERT INTO Dpt_Faculty (faculty_id, admin_id, name, email, department)
        VALUES ({id}, {admin_id}, '{name}', '{email}', '{department}')
        '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added faculty")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of a given faculty from its faculty_id
@system_admin_routes.route('/faculty/<faculty_id>', methods=['GET'])
def get_faculty_info(faculty_id):
    query = f'''
        SELECT faculty_id, admin_id, name, email, department
        FROM Dpt_Faculty
        WHERE faculty_id = {faculty_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    faculty_data = cursor.fetchall()
    response = make_response(jsonify(faculty_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Removes a faculty from the system
@system_admin_routes.route('/faculty/<faculty_id>', methods=['DELETE'])
def delete_faculty(faculty_id):
    query = f'''
    DELETE FROM Dpt_Faculty
    WHERE faculty_id = {faculty_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted faculty")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Gets the info of all admins in the system
@system_admin_routes.route('/', methods=['GET'])
def get_all_admins():
    query = '''
        SELECT *
        FROM System_Admin
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    admin_data = cursor.fetchall()
    return make_response(jsonify(admin_data)), 200

#------------------------------------------------------------
# Gets the info of a system admin from its admin_id
@system_admin_routes.route('/<admin_id>', methods=['GET'])
def get_admin_info(admin_id):
    query = f'''
        SELECT admin_id, name, email, industry, num_applications
        FROM System_Admin
        WHERE admin_id = {admin_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)

    admin_data = cursor.fetchall()
    response = make_response(jsonify(admin_data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Updates the info of an admin given its admin_id
@system_admin_routes.route('/<admin_id>', methods=['PUT'])
def update_admin(admin_id):
    admin_data = request.json

    name = admin_data['name']
    email = admin_data['email']
    industry = admin_data['industry']
    num_apps = admin_data['num_applications']

    query = f'''
    UPDATE System_Admin
    SET name = '{name}',
        email = '{email}',
        industry = '{industry}',
        num_applications = {num_apps}
    WHERE admin_id = {admin_id};    
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully updated admin")
    response.status_code = 200
    return response