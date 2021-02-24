from flask import request, json, jsonify
from src import app, db
from src.models import Competitor, Tournament

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

@app.route('/tournament')
def get_tournament():
    tournament_response = Tournament.query.all()
    tournament_list = []

    for tournament in tournament_response:
        tournament_list.append(tournament.asdict())

    response = jsonify({
        'tournaments': tournament_list
    })

    return response