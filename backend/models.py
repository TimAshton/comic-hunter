from extensions import db
from datetime import datetime
import uuid as uuid_lib
import enum


class ConditionEnum(enum.Enum):
    MINT = "MT"
    NEAR_MINT = "NM"
    VERY_FINE = "VF"
    FINE = "FN"
    VERY_GOOD = "VG"
    GOOD = "GD"
    FAIR = "FR"
    POOR = "PR"


# --- Association (join) tables ---
# These are plain tables, not model classes, since they hold no data
# beyond the foreign key pairs.

comic_writers = db.Table(
    'comic_writers',
    db.Column('comic_id', db.String(36), db.ForeignKey('comic.uuid'), primary_key=True),
    db.Column('writer_id', db.String(36), db.ForeignKey('writer.uuid'), primary_key=True)
)

comic_artists = db.Table(
    'comic_artists',
    db.Column('comic_id', db.String(36), db.ForeignKey('comic.uuid'), primary_key=True),
    db.Column('artist_id', db.String(36), db.ForeignKey('artist.uuid'), primary_key=True)
)

comic_letterers = db.Table(
    'comic_letterers',
    db.Column('comic_id', db.String(36), db.ForeignKey('comic.uuid'), primary_key=True),
    db.Column('letterer_id', db.String(36), db.ForeignKey('letterer.uuid'), primary_key=True)
)


class Comic(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    publication_date = db.Column(db.DateTime)
    acquisition_date = db.Column(db.DateTime, default=datetime.utcnow)

    publisher_id = db.Column(db.String(36), db.ForeignKey('publisher.uuid'), nullable=False)
    publisher = db.relationship('Publisher', backref='comics')

    title = db.Column(db.String(255), nullable=False)
    cover_price = db.Column(db.Numeric(10, 2))
    variant = db.Column(db.String(100))  # was "varient" — typo fix
    asking_price = db.Column(db.Numeric(10, 2))
    condition = db.Column(db.Enum(ConditionEnum), nullable=False)
    notes = db.Column(db.Text)

    # Many-to-many relationships via association tables
    writers = db.relationship('Writer', secondary=comic_writers, backref='comics')
    artists = db.relationship('Artist', secondary=comic_artists, backref='comics')
    letterers = db.relationship('Letterer', secondary=comic_letterers, backref='comics')

    # One-to-many: a comic has a history of many price points over time
    price_history = db.relationship('ComicPriceHistory', backref='comic', order_by='ComicPriceHistory.recorded_at')


class Writer(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    name = db.Column(db.String(255), nullable=False)


class Artist(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    name = db.Column(db.String(255), nullable=False)


class Letterer(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    name = db.Column(db.String(255), nullable=False)


class Publisher(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    name = db.Column(db.String(255), nullable=False)


class ComicPriceHistory(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    comic_id = db.Column(db.String(36), db.ForeignKey('comic.uuid'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)