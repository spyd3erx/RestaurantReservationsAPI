from flask import Blueprint

api = Blueprint("api", __name__)

#customer endpoints
from . import customer

#table endpoints
from . import table

#reservation endpoint
from . import reservation