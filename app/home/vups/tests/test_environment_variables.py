import unittest
import os

FLASK_APP = os.environ['FLASK_APP']
FLASK_ENV = os.environ['FLASK_ENV']

class TestEnvironmentVariables(unittest.TestCase):

    def test_flask_app(self):
        global FLASK_APP
        self.assertEqual(FLASK_APP, 'run.py')

    def test_flask_env(self):
        global FLASK_ENV
        self.assertEqual(FLASK_ENV, 'production')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()