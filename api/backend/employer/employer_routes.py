from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
import json
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data

# This blueprint handles some basic routes that you can use for testing
# BLUEPRINT == COLLECTION OF ROUTES
employer_routes = Blueprint('employer_routes', __name__)

@employer_routes.route('/job_list', methods=['GET'])
def get_job_list(id):
    query = '''
        SELECT 
    '''