from app import db, Video

## CREATE ##
cast = Video('Cast Away')
db.session.add(cast)
db.session.commit()

## READ ##
all_puppies = Video.query.all() # list of puppies objects in the table
print(all_puppies)

# SELECT BY ID
video_one = Video.query.get(1)
print(video_one.title)

# FILTERS
# PRODUCE SOME SQL CODE
cast = Video.query.filter_by(title='Cast Away')
print(cast.all())

# UPDATE
video_one = Video.query.get(1)
video_one.title = 'New Title'
db.session.add(video_one)

# DELETE
second_video = Video.query.get(2)
db.session.delete(second_video)