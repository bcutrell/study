from flask import Flask, render_template, request,session, redirect, url_for, flash
from werkzeug import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class VideoForm(FlaskForm):
  title = StringField('Video Title', validators=[DataRequired()])
  submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
  videos = [
    { 'fpath': 'abc', 'title': 'Video 1', 'upvotes': 1, 'downvotes': 2 }
  ]

  title=False
  form = VideoForm()
  if form.validate_on_submit():
    title = form.title.data
    form.title.data = ''

  else:
    flash('Error')
    # return redirect(url_for('index'))

  return render_template('index.html', videos=videos, form=form, title=title)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
  if request.method == 'POST':
    f = request.files['file']
    f.save('static/' + secure_filename(f.filename))

    # first = request.args.get('first')
    # last = request.args.get('last')

    return 'file uploaded successfully'

@app.route('/video/<name>')
def video(name):
  return "Video: {}".format(name.upper())

def vote():
  pass



@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == '__main__':
  app.run(debug=True)
