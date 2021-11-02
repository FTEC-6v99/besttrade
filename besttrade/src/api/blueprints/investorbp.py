from flask import (Blueprint)
from besttrade.src.api import application

investor_blueprint = bp = Blueprint('investor',__name__, url_prefix='/investor')

@bp.route('/')
def default():
    return '<h1>Yay this works for the investor route!!</h1>'