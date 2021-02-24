from datetime import datetime
from src import db

class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, nullable=False)
    amount_competitors = db.Column(db.Integer)
    amount_match = db.Column(db.Integer)
    amount_round = db.Column(db.Integer)
    
    def asdict(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'amount_competitors': self.amount_competitors, 
            'amount_match': self.amount_match, 
            'amount_round': self.amount_round 
        }

class Competitor(db.Model):
    __tablename__ = 'competitor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, nullable=False)

    def asdict(self):
        return {
            'id': self.id, 
            'name': self.name
        }


class TournamentCompetitor(db.Model):
    __tablename__ = 'tournamentXcompetitor'
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))

    def asdict(self):
        return {
            'id': self.id, 
            'tournament_id': self.tournament_id, 
            'competitor_id': self.competitor_id
        }

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    loser = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    winner = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    match = db.Column(db.Integer)
    round = db.Column(db.Integer)

    def asdict(self):
        return {
            'id': self.id,
            'loser':self.loser,
            'winner':self.winner,
            'tournament_id': self.tournament_id,
            'match': self.match,
            'round': self.round,
        }


class MatchCompetitor(db.Model):
    __tablename__ = 'matchXcompetitor'
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    
    def asdict(self):
        return {
            'id': self.id,
            'match_id':self.match_id,
            'competitor_id': self.competitor_id
        }
