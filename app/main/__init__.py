from flask import Blueprint

main = Blueprint('main', __name__)

from . import gwfy_views, wenbai_views, tss_views, errors
