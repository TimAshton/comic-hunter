from flask import Blueprint

from .models import User
from .extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "BP Avlie"