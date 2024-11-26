
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

# Add new students to the database
@advisors.route('/students/', methods=['POST'])
def get_students():
    # get the request JSON data
    theData = request.json
    # extract student details from the JSON payload
    name = data.get('name')
    age = data.get('age')
    # query to insert a new student record
    query = f"INSERT INTO students (name, age) VALUES ('{name}', {age})"
    # execute the query and commit the changes to the database
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    # return a success message with a 201 HTTP status code
    return make_response("Student added successfully.", 201)

# Remove a student from the database
@routes.route('/student/', methods=['DELETE'])
def delete_student():
    # get the request JSON data
    data = request.json