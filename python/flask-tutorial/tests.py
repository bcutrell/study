from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Video

class UserModelCase(unittest.TestCase):
  def setUp(self):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_password_hashing(self):
    u = User(username='susan')
    u.set_password('cat')
    self.assertFalse(u.check_password('dog'))
    self.assertTrue(u.check_password('cat'))

  def test_videos(self):
    v1 = Video(title='susans movie')
    v2 = Video(title='brians movie')

    db.session.add(v1)
    db.session.add(v2)

    db.session.commit()
    self.assertEqual(Video.load_all(), [v2, v1])

if __name__ == '__main__':
  unittest.main(verbosity=2)
