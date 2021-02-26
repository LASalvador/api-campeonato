from flask import request, json, jsonify
from flask_swagger import swagger
from src import app, db, database
from src.models import Competitor, Tournament, TournamentCompetitor, Match, MatchCompetitor

@app.route('/')
def index():
    """
    Test Server
    ---
    responses:
        200:
            description: Server Works
    """
    return {'status': 'Server Works'}

@app.route('/competitor', methods=['POST'])
def post_competitor():
    """
    Create a competitor
    ---
    tags:
        - Competitor
    parameters:
        - in: body
          name: name
          description: Competitor's name
    responses:
        200:
            description: Competitor Created
    """
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
    """
    Get all Competitors
    ---
    tags:
        - Competitor
    responses:
        200:
            description: All Competitor
    """
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
    """
    Get competitor by ID
    ---
    tags:
        - Competitor
    parameters:
        - name: competitor_id
          in: path
          required: true
          type: int
          description: competitor id
    responses:
        200:
            description: Competitor 
        404:
            description: Resource not found
    """
    competitor = database.get_or_404(Competitor, competitor_id)

    competitor_dict = competitor.asdict()

    response = jsonify({
        'competitor': competitor_dict
    })
    
    return response

@app.route('/tournament', methods=['POST'])
def post_tournament():
    """
    Create tournament
    ---
    tags:
        - Tournament
    parameters:
        - name: name
          in: body
          type: string
          required: true
          description: tournament name
        - name: competitors
          in: body
          type: array
          required: true
          description: array of competitors in the tournament
    responses:
        200:
            description: Created Tournament
        404:
            description: Some Competitor was not Found
    """
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
    """
    Get all Tournaments
    ---
    tags:
        - Tournament
    responses:
        200:
            description: All Tournament
    """
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
    """
    Get Tournament by ID
    ---
    tags:
        - Tournament
    parameters:
        - name: tournament_id
          in: path
          type: int
          required: true
          description: tournament id
    responses:
        200:
            description: Tournament 
        404:
            description: Resource not found
    """
    tournament = database.get_or_404(Tournament, tournament_id)

    tournament_dict = tournament.asdict()

    response = jsonify({
        'tournament': tournament_dict
    })

    return response

@app.route('/tournament/<int:tournament_id>/match')
def get_match_by_tournament(tournament_id):
    """
    Get all Matches from tournament
    ---
    tags: 
        - Tournament
    parameters:
        - name: tournament_id
          in: path
          type: int
          required: true
          description: tournament id
    responses:
        200:
            description: all matches from tournament
    """
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
    """
    Get result (top 4) from tournament
    ---
    tags:
        - Tournament
    parameters:
        - name: tournament_id
          in: path
          type: int
          required: true
          description: tournament id
    responses:
        404:
            description: tournament not found
        400:
            description: tournament was not finished
        200:
            description: top 4 from tournament

    """
    tournament = database.get(Tournament,tournament_id)
    if not tournament:
        return  {"error":"Tournament not found"}, 404
    
    amount_current_matches = Match.query.filter_by(tournament_id=tournament_id).count()
    if amount_current_matches != tournament.amount_match:
        return {"error": "Tournament was not finished"}, 400

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
    """
    Post match
    ---
    tags:
        - Match
    parameters:
        - name: loser
          in: body
          type: int
          required: true
          description: match's loser
        - name: winner
          in: body
          type: int
          required: true
          description: match's winner
        - name: tournament
          in: body
          required: true
          type: int
          description: tournament id
    responses:
        400:
            description: Match OverFlow
        404:
            description: Competitor or Tournament not found
        200:
            description: Created Match
    """
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

    if (next_match_number > tournament.amount_match):
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
    """
    Get all matches
    ---
    tags:
        - Match
    responses:
        200:
            description: all Matches
    """
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
    """
    Get match by id
    --- 
    tags:
        - Match
    parameters:
        - name: match_id
          in: path
          type: int
          required: true
          description: match id
    responses:
        200:
            description: Match 
        404:
            description: resource not found
    """
    match = database.get_or_404(Match, match_id)

    match_dict = match.asdict()

    response = jsonify({
        'match': match_dict
    })

    return response

@app.errorhandler(404)
def not_found(error):
    return {'error': 'resource not found'}, 404


@app.route('/docs')
def get_docs():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "API-Campeonato Docs"
    return jsonify(swag)