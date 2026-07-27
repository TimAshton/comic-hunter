from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    country = db.Column(db.String(100))
    founded_year = db.Column(db.Integer)

class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)  # null if ongoing
    genre = db.Column(db.String(100))

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    issue_number = db.Column(db.String(20))  # string to handle #1/2, annuals etc
    title = db.Column(db.String(255))
    cover_date = db.Column(db.Date)
    cover_image_url = db.Column(db.String(500))
    is_first_appearance = db.Column(db.Boolean, default=False)
    is_key_issue = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asking_price = db.Column(db.Numeric(10, 2))
    condition = db.Column(db.String(10))  # NM, VF, FN, VG, GD, FR, PR
    grade = db.Column(db.Numeric(4, 1))   # CGC grade e.g. 9.8
    is_graded = db.Column(db.Boolean, default=False)
    is_auction = db.Column(db.Boolean, default=False)
    auction_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)