from flask import Blueprint
personal = Blueprint('personal',__name__)
from . import views
from ..main import errors