
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
# Get all the products from the database, package them up,
# and return them to the client
@advisors.route('/advisors/students/', methods=['GET'])
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
    # reate a HTTP Response object and add results of the query to it
    response = make_response(jsonify(theData))
    # send the response back
    return response
