from user import User

users = [
    User(1, 'Jose', 'mypassword')
]

username_table = { u.username: u for u in users }
userid_table = { u.id: u for us in users }

def authenticate(username, password):
    # check if user exists
    user = username_table.get(username, None)

    # if so, return user
    if user and password == user.password:
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

# how to use in Flask
from flask_jwt import JWT, jwt_required
app = Flask(app)
jwt = JWP(app, authenticate, identity)

# Use wrapper in models
@jwt_required()

# post /auth
# {
#   username: username,
#   password: password
# }

# response
# access_token

# Use "JWT access_token" to make seperate API calls