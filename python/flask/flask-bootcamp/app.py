from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
  videos = [
    { 'fpath': 'abc', 'title': 'Video 1', 'upvotes': 1, 'downvotes': 2 }
  ]
  return render_template('index.html', videos=videos)

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
