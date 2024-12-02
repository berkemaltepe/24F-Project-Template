from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a blueprint for employer routes
depthead_routes = Blueprint('depthead_routes', __name__)

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a blueprint for employer routes
depthead_routes = Blueprint('depthead_routes', __name__)

@depthead_routes.route('/avg-student-to-coop/major/<major>', methods=['GET'])
def get_avg_student_to_coop_skills_major(major):
    """
    Endpoint to get average student skill proficiencies and average coop skill requirements.
    """
    query = '''
    SELECT
        sk.skill_name,
        AVG(ss.weight) AS avg_student_proficiency,
        AVG(js.weight) AS avg_skill_weightage
    FROM Student AS s
    JOIN Student_Skill AS ss
        ON s.student_id = ss.student_id
    JOIN Skill AS sk
        ON ss.skill_id = sk.skill_id
    LEFT JOIN Job_Skill AS js
        ON sk.skill_id = js.skill_id
    WHERE
        s.major = %s
    GROUP BY
        sk.skill_name;
    '''
    
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute(query, (major,))
        data = cursor.fetchall()

        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500
    

@depthead_routes.route('/avg-student-to-coop/skill/<skill_name>', methods=['GET'])
def get_avg_student_to_coop_skills_skill(skill_name):
    """
    Endpoint to get average student skill proficiencies and average coop skill requirements.
    """
    query = '''
    SELECT
        sk.skill_name,
        AVG(ss.weight) AS avg_student_proficiency,
        AVG(js.weight) AS avg_skill_weightage
    FROM Student AS s
    JOIN Student_Skill AS ss
        ON s.student_id = ss.student_id
    JOIN Skill AS sk
        ON ss.skill_id = sk.skill_id
    LEFT JOIN Job_Skill AS js
        ON sk.skill_id = js.skill_id
    WHERE
        sk.skill_name = %s
    GROUP BY
        sk.skill_name;
    '''
    
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute(query, (skill_name,))
        data = cursor.fetchone()

        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

@depthead_routes.route('/top-skills', methods=['GET'])
def get_top_skills():
    """
    Endpoint to get the most commonly required skills for co-ops.
    """

    query = '''
SELECT
    sk.skill_name,
    sk.skill_type,
    COUNT(js.skill_id) AS frequency,
    AVG(js.weight) AS avg_importance,
    AVG(ss.weight) AS avg_student_proficiency,
    AVG(js.weight) AS avg_skill_weightage
FROM
    Skill AS sk
JOIN
    Job_Skill AS js ON sk.skill_id = js.skill_id
LEFT JOIN
    Student_Skill AS ss ON sk.skill_id = ss.skill_id  -- Assuming you want all skills even if no student has it
LEFT JOIN
    Student AS s ON ss.student_id = s.student_id      -- Join to get student data for proficiency
GROUP BY
    sk.skill_name, sk.skill_type
ORDER BY
    frequency DESC, avg_importance DESC;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute(query)
        data = cursor.fetchall()

        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500
    

@depthead_routes.route('all-job-skills', methods=['GET'])
def get_all_jobs_with_skills():
    """
    Endpoint to get all job listings and their skill requirements.
    """

    query = '''
    SELECT
        j.title AS job_title,
        e.name AS employer_name,
        sk.skill_name,
        js.weight AS skill_importance
    FROM Job AS j
    JOIN Employer AS e
        ON j.emp_id = e.emp_id
    LEFT JOIN Job_Skill AS js
        ON j.job_id = js.job_id
    LEFT JOIN Skill AS sk
        ON js.skill_id = sk.skill_id
    ORDER BY
        j.job_id;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query
        cursor.execute(query)
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

@depthead_routes.route('all-student-skills', methods=['GET'])
def get_all_student_skills():
    """
    Endpoint to get all students and their skill proficiencies
    """
    
    query = '''
    SELECT
        s.student_id,
        s.name AS student_name,
        sk.skill_name,
        ss.weight AS proficiency_level
    FROM Student AS s
    LEFT JOIN Student_Skill AS ss
        ON s.student_id = ss.student_id
    LEFT JOIN Skill AS sk
        ON ss.skill_id = sk.skill_id
    ORDER BY
        s.student_id;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query
        cursor.execute(query)
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

@depthead_routes.route('top-tools/<skill_type>', methods=['GET'])
def get_top_tools(skill_type):
    """
    Endpoint to get the most in-demand tools in a specific skill type
    """
    query = '''
    SELECT
        sk.skill_name,
        sk.skill_type,
        COUNT(js.skill_id) AS frequency,
        AVG(js.weight) AS avg_importance
    FROM Job_Skill AS js
    JOIN Skill AS sk
        ON js.skill_id = sk.skill_id
    WHERE
        sk.skill_type IN (%s)
    GROUP BY
        sk.skill_name, sk.skill_type
    ORDER BY
        frequency DESC, avg_importance DESC;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query with the skill_type parameter
        cursor.execute(query, (skill_type,))
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

@depthead_routes.route('skill/skill_type', methods=['GET'])
def get_all_skill_types():
    """
    Endpoint to get all skill types that exist.
    """

    query = '''
    SELECT DISTINCT
        sk.skill_type
    FROM 
        Skill sk
    ORDER BY sk.skill_type ASC 
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query with the skill_name parameter
        cursor.execute(query)
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500
    

@depthead_routes.route('avg-req-weight/<skill_name>', methods=['GET'])
def get_avg_req_weight(skill_name):
    """
    Endpoint to get the average required proficiency weight for a specific skill.
    """

    query = '''
    SELECT 
        sk.skill_name, 
        AVG(js.weight) AS avg_required_proficiency 
    FROM 
        Skill sk 
    JOIN 
        Job_Skill js 
        ON sk.skill_id = js.skill_id 
    WHERE 
        sk.skill_name = %s 
    GROUP BY 
        sk.skill_name;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query with the skill_name parameter
        cursor.execute(query, (skill_name,))
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500
