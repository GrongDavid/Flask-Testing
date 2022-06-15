from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homeboard(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('times_played'))
            self.assertIn('Score:', response.data)
            self.assertIn('Time left:', response.data)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["f", "r", "o", "m", "t"], 
                                 ["k", "o", "q", "n", "h"], 
                                 ["l", "a", "t", "m", "s"], 
                                 ["j", "d", "z", "g", "a"], 
                                 ["t", "z", "x", "b", "v"]]
        response = self.client.get('/check-word?word=from')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=robot')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_real_word(self):
        self.client.get('/')
        response = self.client.get(
            '/check-word?word=sjdksjsdf')
        self.assertEqual(response.json['result'], 'not-word')