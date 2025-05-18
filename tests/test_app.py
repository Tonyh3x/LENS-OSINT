import unittest
from app import app
import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LENS OSINT ANALYZER', response.data)

    def test_analyze_files(self):
        test_file = open('tests/test_files/sample.txt', 'rb')
        
        response = self.app.post(
            '/analyze',
            data={
                'files[]': [test_file]
            },
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertIn('errors', data)
        
        test_file.close()

    def test_file_limit(self):
        test_files = [
            open('tests/test_files/sample.txt', 'rb')
            for _ in range(6)
        ]
        
        response = self.app.post(
            '/analyze',
            data={
                'files[]': test_files
            },
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Maximum 5 files allowed')
        
        for file in test_files:
            file.close()

    def test_invalid_file_type(self):
        test_file = open('tests/test_files/invalid_file.exe', 'rb')
        
        response = self.app.post(
            '/analyze',
            data={
                'files[]': [test_file]
            },
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Invalid file type', data['errors'][0])
        
        test_file.close()

    def test_file_size_limit(self):
        test_file = open('tests/test_files/large_file.txt', 'rb')
        
        response = self.app.post(
            '/analyze',
            data={
                'files[]': [test_file]
            },
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 413)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'File too large')
        
        test_file.close()

if __name__ == '__main__':
    unittest.main()
