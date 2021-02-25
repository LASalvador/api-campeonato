from flask import request, json, jsonify
from src import app, db, database
from src.models import Competitor, Tournament, TournamentCompetitor, Match, MatchCompetitor

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
    # validar a existencia desses caras
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


@app.route('/match', methods=['POST'])
def post_match():
    data = request.json
    # validar a existencia desses caras
    loser = data['loser']
    winner = data['winner']
    tournament_id =  data['tournament']
    # gerar esse número automaticamente de acordo com registro desse torneio
    match_number = data['match']

    match = database.add_instance(Match, loser=loser, winner=winner,tournament_id=tournament_id, match = match_number)

    database.add_instance(MatchCompetitor, match_id = match.id, competitor_id = winner)
    database.add_instance(MatchCompetitor, match_id = match.id, competitor_id = loser)

    match_dict = match.asdict()

    response = jsonify({
        'match': match_dict
    })

    return response

@app.route('/match')
def get_match():
    match_response = database.get_all(Match)
    match_list = []

    for match in match_response:
        match_list.append(match.asdict())

    response = jsonify({
        'match': match_list
    })

    return response


@app.route('/match/<int:match_id>')
def get_match_by_id(match_id):
    match = database.get_by_id(Match, match_id)

    match_dict = match.asdict()

    response = jsonify({
        'match': match_dict
    })

    return response
