from flask import Blueprint

posts = Blueprint('post', __name__)

from . import routes
