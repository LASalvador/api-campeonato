from flask import request, json, jsonify
from src import app, db, database
from src.models import Competitor, Tournament, TournamentCompetitor

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

@app.route('/competitor/<int:competitor_id>')
def get_competitor_by_id(competitor_id):
    competitor = database.get_by_id(Competitor, competitor_id)

    competitor_dict = competitor.asdict()

    response = jsonify({
        'competitor': competitor_dict
    })
    
    return response

@app.route('/tournament', methods=['POST'])
def post_tournament():
    data = request.json
    name = data['name']
    competitors = data['competitors']
    amount_match = len(competitors)
    amount_competitors = len(competitors)

    tournament = database.add_instance(Tournament, name=name, amount_match = amount_match, amount_competitors = amount_competitors)

    for competitor in competitors:
        database.add_instance(TournamentCompetitor, tournament_id=tournament.id, competitor_id = competitor)

    tournament_dict = tournament.asdict()

    response = jsonify({
        'tournament': tournament_dict
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


@app.route('/tournament/<int:tournament_id>')
def get_tournament_by_id(tournament_id):
    tournament = database.get_by_id(Tournament, tournament_id)

    tournament_dict = tournament.asdict()

    response = jsonify({
        'tournament': tournament_dict
    })

    return response