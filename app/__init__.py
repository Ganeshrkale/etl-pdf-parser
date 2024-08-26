from flask import Flask
from flask_cors import CORS
import tracemalloc


app = Flask(__name__)
CORS(app)
tracemalloc.start()

from app.controllers.parser_controller import *
