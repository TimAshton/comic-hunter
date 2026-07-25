from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, ma
from models import Comic, Writer, Artist, Letterer, Publisher, ComicPriceHistory

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    CORS(app)

    # blueprints get registered here once you write routes/comics.py
    # from routes.comics import comics_bp
    # app.register_blueprint(comics_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)