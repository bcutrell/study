from app import db, Video

# Creates tables Model --> Db Table
db.create_all()

cast = Video('Cast Away')
print(cast.id) # None
db.session.add_all([cast]) # db.session.add(cast)

db.session.commit()
print(cast.id)


# MIGRATIONS
# export FLASK_APP=app.py
# flask db init
# flask db migrate -m "some message"
# flask db upgrade
