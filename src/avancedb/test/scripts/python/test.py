import couchdb
import unittest
import requests

host = 'http://localhost'
port = '15994'
url = host + ':' + port
couch = couchdb.Server(url)

    
class ServerInfoTestCase(unittest.TestCase):

    def test_validate_server_signature(self):
        r = requests.get(url + '/')
        self.assertEqual(r.json(), {
                "couchdb":"Welcome",
                "avancedb":"Welcome",
                "uuid":"a2db86472466bcd02e84ac05a6c86185",
                "version":"1.6.1",
                "vendor":{
                    "version":"0.0.1", "name":"Ripcord Software"
                }
            })
            
class FutonTestCase(unittest.TestCase):
    
    def test_redirect(self):
        r = requests.get(url + '/_utils', allow_redirects=False)
        self.assertEqual(r.status_code, 307)
        self.assertEqual(r.headers['location'], '/_utils/index.html')
    
    def test_get_html(self):
        r = requests.get(url + '/_utils')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'text/html')
    
    def test_get_favicon(self):
        r = requests.get(url + '/_utils/favicon.ico')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'image/ico')
    
    def test_get_logo(self):
        r = requests.get(url + '/_utils/image/logo.png')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'image/png')
    
    def test_not_valid_response(self):
        r = requests.get(url + '/_utils/nothing_to_see_here')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.headers['content-length'], '0')

if __name__ == "__main__":
    unittest.main() # run all tests
