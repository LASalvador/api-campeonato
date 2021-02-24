from flask import request, json, jsonify
from src import app, db
from src.models import Competitor

@app.route('/')
def index():
    return 'Server Works!!'

@app.route('/competitor')
def get_competitor():
    
    competitor_response = Competitor.query.all()
    competitor_list = []

    for competitor in competitor_response:
        competitor_list.append(competitor.asdict())

    response = jsonify({
        'competitors': competitor_list
    })

    return response