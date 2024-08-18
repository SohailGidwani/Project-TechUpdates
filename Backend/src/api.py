import utility
from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_apscheduler import APScheduler

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/scrape_and_categorize', methods=['POST'])
def scrape_and_categorize():
    # from app import scheduler
    # job_id = f"scrape_and_categorize_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    # scheduler.add_job(id=job_id, func=utility.scrape_and_categorize, trigger='date')
    # return jsonify({'message': 'Scraping and categorization process started'}), 202
    result = utility.scrape_and_categorize()
    return jsonify(result), 200

@api_blueprint.route('/upload_to_qdrant', methods=['POST'])
def upload_to_qdrant():
    result = utility.upload_to_qdrant()
    return jsonify(result), 200

@api_blueprint.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    result = utility.search(query)
    return jsonify(result), 200
