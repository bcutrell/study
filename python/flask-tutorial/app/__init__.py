from flask import Flask

app = Flask(__name__)

# workaround for circular imports
from app import routes
