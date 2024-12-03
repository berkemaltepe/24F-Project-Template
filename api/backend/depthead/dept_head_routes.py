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

@depthead_routes.route('/top-student-skills/<major>', methods=['GET'])
def get_top_student_skills(major):
    """
    Endpoint to get the most commonly occuring skills for students
    """

    query = '''
    SELECT 
        sk.skill_name,
        sk.skill_type,
        sk.skill_id,
        COUNT(ss.skill_id) AS frequency,
        AVG(ss.weight) AS avg_student_proficiency
    FROM 
        Skill AS sk
    JOIN 
        Student_Skill AS ss ON sk.skill_id = ss.skill_id
    LEFT JOIN
    Student AS s ON ss.student_id = s.student_id
    WHERE 
    s.major = (%s)
    GROUP BY 
    sk.skill_name, sk.skill_type, sk.skill_id
    ORDER BY 
        frequency DESC, avg_student_proficiency DESC;
                '''
    
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query with the skill_type parameter
        cursor.execute(query, (major,))
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
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
    sk.skill_id,
    COUNT(js.skill_id) AS frequency,
    AVG(ss.weight) AS avg_student_proficiency,
    AVG(js.weight) AS avg_skill_weightage
FROM
    Skill AS sk
JOIN
    Job_Skill AS js ON sk.skill_id = js.skill_id
LEFT JOIN
    Student_Skill AS ss ON sk.skill_id = ss.skill_id  
LEFT JOIN
    Student AS s ON ss.student_id = s.student_id      -- Join to get student data for proficiency
GROUP BY
    sk.skill_name, sk.skill_type, sk.skill_id
ORDER BY
    frequency DESC, avg_skill_weightage DESC;
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
    
@depthead_routes.route('job/industry', methods=['GET'])
def get_all_industries():
    """
    Endpoint to get all industries.
    """

    query = '''
    SELECT DISTINCT
        j.industry
    FROM Job AS j
    ORDER BY j.industry ASC
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


@depthead_routes.route('all-job-skills', methods=['GET'])
def get_all_jobs_with_skills():
    """
    Endpoint to get all job listings and their skill requirements.
    """

    query = '''
    SELECT
        j.job_id,
        j.description,
        j.title AS job_title,
        e.name AS employer_name,
        j.industry,
        j.pay_range,
        j.date_posted,
        j.status
    FROM Job AS j
    JOIN Employer AS e
        ON j.emp_id = e.emp_id
    ORDER BY
        employer_name;
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

@depthead_routes.route('/jobs/<job_id>/skills', methods=['GET'])
def get_job_skills(job_id):
    """
    Endpoint to fetch required skills for a specific job.
    """
    try:
        cursor = db.get_db().cursor()
        # Database query to fetch job-required skills
        query = """
        SELECT sk.skill_id, sk.skill_name, js.weight
        FROM Job_Skill AS js
        JOIN Skill AS sk ON js.skill_id = sk.skill_id
        WHERE js.job_id = %s;
        """
        cursor.execute(query, (job_id,))
        # Transform query results into JSON response
        results = cursor.fetchall()

        # Ensure proper keys in the response
        return make_response(jsonify(results)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@depthead_routes.route('/student/<student_id>/skills', methods=['GET'])
def get_student_skills(student_id):
    """
    Endpoint to fetch required skills for a specific student.
    """
    try:
        cursor = db.get_db().cursor()
        # Database query to fetch job-required skills
        query = """
        SELECT sk.skill_id, sk.skill_name, ss.weight
        FROM Student_Skill AS ss
        JOIN Skill AS sk ON ss.skill_id = sk.skill_id
        WHERE ss.student_id = %s;
        """
        cursor.execute(query, (student_id,))
        # Transform query results into JSON response
        results = cursor.fetchall()

        # Ensure proper keys in the response
        return make_response(jsonify(results)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@depthead_routes.route('all-job-skills/<skill_name>', methods=['GET'])
def get_all_jobs_with_skill(skill_name):
    """
    Endpoint to get all job listings and their skill requirements.
    """

    query = '''
    SELECT
        j.job_id,
        j.description,
        j.title AS job_title,
        e.name AS employer_name,
        js.weight AS skill_importance,
        j.industry,
        j.pay_range,
        j.date_posted,
        j.status
    FROM Job AS j
    JOIN Employer AS e
        ON j.emp_id = e.emp_id
    LEFT JOIN Job_Skill AS js
        ON j.job_id = js.job_id
    LEFT JOIN Skill AS sk
        ON js.skill_id = sk.skill_id
    WHERE 
        sk.skill_name = (%s)
    ORDER BY
        j.job_id;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query
        cursor.execute(query, (skill_name, ))
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

@depthead_routes.route('all-student-skills/<skill_name>', methods=['GET'])
def get_students_with_skill(skill_name):
    """
    Endpoint to get all students
    """
    
    query = '''
    SELECT
        s.student_id,
        s.email,
        s.name AS student_name,
        s.major,
        s.coop_status,
        s.gpa,
        s.level
    FROM Student AS s
    LEFT JOIN Student_Skill AS ss
        ON s.student_id = ss.student_id
    LEFT JOIN Skill AS sk
        ON ss.skill_id = sk.skill_id
    WHERE 
        sk.skill_name = (%s)
    ORDER BY
        s.student_id;
    '''


    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query
        cursor.execute(query, (skill_name))
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
    Endpoint to get all students
    """
    
    query = '''
    SELECT
        s.student_id,
        s.email,
        s.name AS student_name,
        s.major,
        s.coop_status,
        s.gpa,
        s.level
    FROM Student AS s
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
    sk.skill_id,
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
WHERE 
    sk.skill_type = (%s)
GROUP BY
    sk.skill_name, sk.skill_type, sk.skill_id
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


@depthead_routes.route('top-skills/industry/<industry>', methods=['GET'])
def get_top_skills_industry(industry):
    """
    Endpoint to get the most in-demand tools in a specific skill type
    """
    query = '''
SELECT
    sk.skill_name,
    sk.skill_type,
    j.industry,
    COUNT(js.skill_id) AS frequency,
    AVG(js.weight) AS avg_importance,
    AVG(ss.weight) AS avg_student_proficiency,
    AVG(js.weight) AS avg_skill_weightage
FROM
    Skill AS sk
JOIN
    Job_Skill AS js ON sk.skill_id = js.skill_id
LEFT JOIN
    Student_Skill AS ss ON sk.skill_id = ss.skill_id  
LEFT JOIN
    Student AS s ON ss.student_id = s.student_id      
LEFT JOIN 
    Job AS j ON js.job_id = j.job_id
WHERE 
    j.industry = (%s)
GROUP BY
    sk.skill_name, sk.skill_type, j.industry
ORDER BY
    frequency DESC, avg_importance DESC;
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query with the skill_type parameter
        cursor.execute(query, (industry,))
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

@depthead_routes.route('student/major', methods=['GET'])
def get_all_majors():
    """
    Endpoint to get all majors that exist.
    """

    query = '''
    SELECT DISTINCT
        s.major
    FROM 
        Student s
    ORDER BY s.major ASC 
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
    

@depthead_routes.route('skill/skill_name', methods=['GET'])
def get_all_skills():
    """
    Endpoint to get all skill names that exist.
    """

    query = '''
    SELECT DISTINCT
        sk.skill_name
    FROM 
        Skill sk
    ORDER BY sk.skill_name ASC 
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

@depthead_routes.route('skill_note/<skill_id>/<faculty_id>', methods=['GET'])
def get_skill_notes(skill_id, faculty_id):
    """
    Endpoint to get all skill notes associated with a certain skill and department head 
    """

    query = '''
    SELECT 
        sk.skill_name,
        note.note_id,
        note.description
    FROM 
        Skill_Note note
    JOIN 
        Skill sk ON sk.skill_id = note.skill_id
    WHERE 
        note.skill_id = %s AND
        note.faculty_id = %s
    '''

    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Execute the query with the skill_id and faculty_id parameters
        cursor.execute(query, (skill_id, faculty_id))
        data = cursor.fetchall()

        # Return the results as a JSON response
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        # Log and return an error if something goes wrong
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500

#Add note
@depthead_routes.route('/skill_note/<faculty_id>/<skill_id>/<description>', methods=['POST'])
def add_skill_note(faculty_id, skill_id, description):
    try:
        # Log input parameters for debugging
        current_app.logger.debug(f"Adding skill note for faculty_id={faculty_id}, skill_id={skill_id}, description={description}")
        
        # Construct query
        query = '''
            INSERT INTO Skill_Note (faculty_id, skill_id, description)
            VALUES (%s, %s, %s);
        '''
        
        # Execute query
        cursor = db.get_db().cursor()
        cursor.execute(query, (faculty_id, skill_id, description))
        db.get_db().commit()
        
        # Verify insert by selecting the note
        cursor.execute("SELECT * FROM Skill_Note WHERE faculty_id=%s AND skill_id=%s AND description=%s", (faculty_id, skill_id, description))
        result = cursor.fetchall()
        if result:
            current_app.logger.debug(f"Skill note inserted: {result}")
        
        return jsonify({"message": "Skill note added successfully"}), 201
    
    except Exception as e:
        current_app.logger.error(f"Error adding note: {e}")
        return jsonify({"error": str(e)}), 400


#Update note
@depthead_routes.route('skill_note/<note_id>/<description>', methods=['PUT'])
def update_skill_note(note_id, description):
    try:
        # Construct query
        query = '''
            UPDATE Skill_Note
            SET description = (%s)
            WHERE note_id = (%s);
        '''
        
        # Execute query
        cursor = db.get_db().cursor()
        cursor.execute(query, (description, note_id))
        db.get_db().commit()
        
        return jsonify({"message": "Skill note added successfully"}), 201
    
    except Exception as e:
        current_app.logger.error(f"Error adding note: {e}")
        return jsonify({"error": str(e)}), 400

#Delete note
@depthead_routes.route('skill_note/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        # Construct query
        query = '''
            DELETE FROM Skill_Note
            WHERE note_id = (%s)
        '''
        
        # Execute query
        cursor = db.get_db().cursor()
        cursor.execute(query, (note_id,))
        db.get_db().commit()
        
        return jsonify({"message": "Skill note deleted successfully"}), 201
    
    except Exception as e:
        current_app.logger.error(f"Error deleting note: {e}")
        return jsonify({"error": str(e)}), 400


