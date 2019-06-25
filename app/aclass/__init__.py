from flask import Blueprint
aclass = Blueprint('aclass',__name__)
from . import views
from ..main import errors