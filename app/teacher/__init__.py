from flask import Blueprint
teacher = Blueprint('teacher',__name__)
from . import views
from ..main import errors