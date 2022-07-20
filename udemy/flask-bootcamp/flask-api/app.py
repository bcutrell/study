from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

videos = [{'name': 'Cast Away'}]

class Videos(Resource):
    def get(self, name):
        print(videos)

        for video in videos:
            if video['name'] == name:
                return video
        
        return {'name': None}, 404

api.add_resource(Videos, '/videos/<string:name>')


if __name__ == '__main__':
    app.run(debug=True)