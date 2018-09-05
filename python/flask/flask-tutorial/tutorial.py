# export FLASK_APP=tutorial.py
# flask run

# command pre-imports the application instance.
# flask shell

# bokeh
# quandl - stocks
# DB - config
#    - seed
#    - select

from app import app, db
from app.models import User, Video

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Video': Video}
