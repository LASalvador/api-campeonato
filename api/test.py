import unittest
import json
from src import app, db

class TestHome(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.response = self.client.get('/')

        with self.app.app_context():
            db.create_all()

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content_type(self):
        self.assertIn('application/json', self.response.content_type)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class TestCompetitor(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.competitor = json.dumps({'name': 'Lucas'})
        with self.app.app_context():
            db.create_all()

    def test_post_competitor(self):
        res = self.client.post('/competitor', data=self.competitor, content_type='application/json')
        self.assertEqual(res.status_code,200)
        self.assertIn('Lucas', str(res.data))

    def test_get_all_competitor(self):
        res = self.client.post('/competitor', data=self.competitor, content_type='application/json')
        self.assertEqual(res.status_code,200)

        res = self.client.get('/competitors')
        self.assertEqual(res.status_code,200)
        self.assertIn('Lucas', str(res.data))

    def test_get_one_competitor(self):
        res = self.client.post('/competitor', data=self.competitor, content_type='application/json')
        self.assertEqual(res.status_code,200)

        id = res.data['id']

        res = self.client.get(f'/competitor/{id}')
        self.assertEqual(res.status_code,200)
        self.assertIn(id, str(res.data))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()