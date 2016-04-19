from ortelius import db
from ortelius.models.Coordinates import Shape
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact

hist_regions_facts = db.Table('hist_regions_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id'))
)

hist_places_facts = db.Table('hist_places_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('hist_place_id', db.Integer, db.ForeignKey('hist_place.id'))
)

Shape.hist_region_id = db.Column(db.Integer, db.ForeignKey('hist_region.id'))
Date.hist_region_id = db.Column(db.Integer, db.ForeignKey('hist_region.id'))
Date.hist_place_id = db.Column(db.Integer, db.ForeignKey('hist_place.id'))


class HistRegion(db.Model):
    """HistRegion model"""
    __tablename__ = 'hist_region'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 text=None,
                 start_date=None,
                 end_date=None,
                 facts=None,
                 shapes=None):
        self.name = name
        self.label = label
        self.description = description
        self.text = text
        self.start_date = start_date
        self.end_date = end_date
        self.facts = facts
        self.shapes = shapes

    text = db.Column(db.UnicodeText, server_default="No text")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    label = db.Column(db.Unicode(255))
    description = db.Column(db.UnicodeText, server_default="No description")
    start_date = db.relationship('Date', backref=db.backref('hist_regions_start', lazy='joined'))
    end_date = db.relationship('Date', backref=db.backref('hist_regions_end', lazy='joined'))
    shapes = db.relationship('Shape', backref=db.backref('hist_region'), lazy='dynamic')
    facts = db.relationship('Fact', secondary=hist_regions_facts, backref=db.backref('hist_regions'), lazy='dynamic')


class HistPlace(db.Model):
    """HistPlace model"""
    __tablename__ = 'hist_place'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 text=None,
                 start_date=None,
                 end_date=None,
                 facts=None):
        self.name = name
        self.label = label
        self.description = description
        self.text = text
        self.start_date = start_date
        self.end_date = end_date
        self.facts = facts

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    label = db.Column(db.Unicode(255))
    description = db.Column(db.UnicodeText, server_default="No description")
    start_date = db.relationship('Date', backref=db.backref('hist_place_start', lazy='joined'))
    end_date = db.relationship('Date', backref=db.backref('hist_place_end', lazy='joined'))
    facts = db.relationship('Fact', secondary=hist_places_facts, backref=db.backref('hist_places'), lazy='dynamic')
