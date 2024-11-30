from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a blueprint for employer routes
depthead_routes = Blueprint('depthead_routes', __name__)

@depthead_routes.route('/avg-student-to-coop', methods=['GET'])
def get_avg_student_to_coop_skills():
    """
    Endpoint to get average student skill proficiencies and average coop skill requirements.
    """
    query = '''
    SELECT
        sk.skill_name,
        AVG(ss.proficiency) AS avg_student_proficiency,
        AVG(js.weight) AS avg_skill_weightage
    FROM Student AS s
    JOIN Student_Skill AS ss
        ON s.student_id = ss.student_id
    JOIN Skill AS sk
        ON ss.skill_id = sk.skill_id
    LEFT JOIN Job_Skill AS js
        ON sk.skill_id = js.skill_id
    WHERE
        s.major = 'Computer Science' -- Filter for Khoury students
    GROUP BY
        sk.skill_name;
    '''
    
    try:
        # Get a database connection
        cursor = db.get_db().cursor()
        
        # Query the database for student skills
        cursor.execute(query)
        data = cursor.fetchall()

        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    
    except Exception as e:
        current_app.logger.error(f"Error fetching information: {e}")
        return jsonify({"error": str(e)}), 500
