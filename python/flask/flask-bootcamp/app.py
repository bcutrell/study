
from flask import Flask, render_template, request,session, redirect, url_for, flash
from werkzeug import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

import os
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
# __file__ --> /Users/../../flask-bootcamp/basic.py

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

########################################################################

class Video(db.Model):
  __tablename__ = 'videos'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text)
  upvotes = db.Column(db.Integer)

  def __init__(self, title, upvotes):
    self.title = title
    self.upvotes = upvotes

  def __repr__(self):
    return f"Video title: {self.title}"

########################################################################

class VideoForm(FlaskForm):
  title = StringField('Video Title', validators=[DataRequired()])
  submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
  title=False
  form = VideoForm()
  if form.validate_on_submit():
    db.session.add(Video(form.title.data, 0))
    db.session.commit()
    form.title.data = ''
    title=False

  else:
    flash('Please Enter a Title')

  videos = Video.query.all()
  return render_template('index.html', videos=videos, form=form, title=title)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
  if request.method == 'POST':
    f = request.files['file']
    f.save('static/' + secure_filename(f.filename))

    # first = request.args.get('first')
    # last = request.args.get('last')

    return 'file uploaded successfully'

@app.route('/video/<title>')
def video(title):
  return "Video: {}".format(title.upper())

@app.route('/delete/<title>', methods=['GET', 'POST'])
def delete(title):
  print(title)
  videos = Video.query.filter_by(title=title)
  [db.session.delete(video) for video in videos]
  db.session.commit()

  return redirect(url_for('index'))



@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == '__main__':
  app.run(debug=True)
