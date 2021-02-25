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

@app.route('/competitors')
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
    competitor = database.get_or_404(Competitor, competitor_id)

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
    
    competitors_target = db.session.query(Competitor).filter(Competitor.id.in_(competitors)).all()

    if len(competitors_target) != len(competitors):
        return {"error":'Some Competitor was not Found'}, 404

    tournament = database.add_instance(Tournament, name=name, amount_match = amount_match, amount_competitors = amount_competitors)
    
    for competitor in competitors:
        database.add_instance(TournamentCompetitor, tournament_id=tournament.id, competitor_id = competitor)

    tournament_dict = tournament.asdict()

    response = jsonify({
        'tournament': tournament_dict
    })

    return response

@app.route('/tournaments')
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
    tournament = database.get_or_404(Tournament, tournament_id)

    tournament_dict = tournament.asdict()

    response = jsonify({
        'tournament': tournament_dict
    })

    return response

@app.route('/tournament/<int:tournament_id>/match')
def get_match_by_tournament(tournament_id):
    matches = Match.query.filter_by(tournament_id=tournament_id).all()
    
    match_list = []

    for match in matches:
        match_list.append(match.asdict())

    response = jsonify({
        'match': match_list
    })

    return response

@app.route('/tournament/<int:tournament_id>/result')
def get_tournament_result(tournament_id):
    # validar se o campeonato já terminou
    last_matches = Match.query.filter_by(tournament_id=tournament_id).order_by(Match.match.desc()).limit(2)
    result = {}
    result[1] = last_matches[0].winner
    result[2] = last_matches[0].loser
    result[3] = last_matches[1].winner
    result[4] = last_matches[1].loser
    
    response = jsonify({
        'result': result
    })

    return response

@app.route('/match', methods=['POST'])
def post_match():
    data = request.json
    loser = data['loser']
    winner = data['winner']
    tournament_id =  data['tournament']

    if not database.get(Competitor,loser) or not database.get(Competitor,winner):
        return {"error":"Competitor(winner or loser) not found"}, 404
    tournament = database.get(Tournament,tournament_id)
    if not tournament:
        return  {"error":"Tournament not found"}, 404

    before_match_number = Match.query.filter_by(tournament_id=tournament_id).count()
    next_match_number = before_match_number + 1

    if (next_match_number >= tournament.amount_match):
        return {"error":'Match OverFlow'}, 400

    match = database.add_instance(Match, loser=loser, winner=winner,tournament_id=tournament_id, match = next_match_number)

    database.add_instance(MatchCompetitor, match_id = match.id, competitor_id = winner)
    database.add_instance(MatchCompetitor, match_id = match.id, competitor_id = loser)

    match_dict = match.asdict()

    response = jsonify({
        'match': match_dict
    })

    return response

@app.route('/matches')
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
    match = database.get_or_404(Match, match_id)

    match_dict = match.asdict()

    response = jsonify({
        'match': match_dict
    })

    return response

@app.errorhandler(404)
def not_found(error):
    return {'error': 'resource not found'}, 404
