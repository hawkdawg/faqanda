from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import *


class Model(unittest.TestCase):

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

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=robohash&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_tag(self):
        t1 = Tag(name='Linux')
        db.session.add(t1)

        t2 = Tag(name='BASH')
        db.session.add(t2)

        db.session.commit()
        q1 = Question(q_title='Who is Tux?', body='Who is Tux? Is he Satoshi Nakamoto?')
        db.session.add(q1)

        self.assertEqual(False, q1.is_tagged(tag=t1))

        q1.tag_question(tag=t1)

        self.assertEqual(True, q1.is_tagged(tag=t1))
        self.assertEqual(False, q1.is_tagged(tag=t2))

        q1.tag_question(tag=t2)

        self.assertEqual([t1, t2], q1.tags.all())


        self.assertEqual([q1], t1.questions.all())

        q1.untag_question(tag=t1)
        q1.untag_question(tag=t2)

        self.assertEqual([], q1.tags.all())














if __name__ == '__main__':
    unittest.main()
    #t = Model()
    #t.test_tag()
