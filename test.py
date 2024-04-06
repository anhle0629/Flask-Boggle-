from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config["testing"] = True
    
    def test_homepage(self):
       
        with self.client:
            repsonse = self.client.get("/")
            
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("nplays"))
            self.assertIn(b'<p>High Score:', repsonse.data)
            self.assertIn(b"Score:", repsonse.data)
            self.assertIn(b"Second_Left:", repsonse.data)

    def test_valid_words(self):
         #Test if word is valid by modifying the board in the session
        with self.client as client:
            with client.session_transaction() as sess:
                sess["board"] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
            response = self.client.get('/check-word?word=cat')
            self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        with self.client.get("/"):
            response = self.client.get("/check-word? word=impossible")
        self.assertEqual(response.json["result"], 'not-on-board')
    
    def non_english_word(self):
        self.client.get("/")
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json["result"], 'not-a-word')



