from flask import Blueprint

main = Blueprint('main', __name__)

from . import gwfy_views, zangjing_views, errors
