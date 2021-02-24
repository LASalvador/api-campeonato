from flask import request, json, jsonify
from src import app, db, database
from src.models import Competitor, Tournament

@app.route('/')
def index():
    return 'Server Works!!'

@app.route('/competitor', methods=['POST'])
def post_competitor():
    data = request.json
    name = data['name']

    competitor = database.add_instance(Competitor, name=name)
    
    competitor_dict = competitor.asdict()

    response = jsonify({
        'competitor': competitor_dict
    })

    return response

@app.route('/competitor')
def get_competitor():

    competitor_response = database.get_all(Competitor)
    competitor_list = []

    for competitor in competitor_response:
        competitor_list.append(competitor.asdict())

    response = jsonify({
        'competitors': competitor_list
    })

    return response

@app.route('/tournament')
def get_tournament():
    tournament_response = database.get_all(Tournament)
    tournament_list = []

    for tournament in tournament_response:
        tournament_list.append(tournament.asdict())

    response = jsonify({
        'tournaments': tournament_list
    })

    return response