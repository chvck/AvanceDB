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

class ConfigTestCase(unittest.TestCase):

    def test_query_servers(self):
        r = requests.get(url + '/_config/query_servers')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertNotEqual(r.json()[u'javascript'], None)

    def test_native_query_servers(self):
        r = requests.get(url + '/_config/native_query_servers')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(r.json(), {})
    
class TasksTestCase(unittest.TestCase):

    def test_no_tasks(self):
        tasks = couch.tasks();
        self.assertNotEqual(tasks, None)
        self.assertEqual(len(tasks), 0)

class SessionTestCase(unittest.TestCase):

    def test_session_response(self):
        r = requests.get(url + '/_session')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        json = r.json()
        self.assertNotEqual(json[u'ok'], None)
        self.assertNotEqual(json[u'userCtx'], None)
        
#class UuidTestCase(unittest.TestCase):

	#def test_get_one_uuid(self):
		#uuids = couch.uuids(1)
		#self.assertEqual(len(uuids), 1)

	#def test_get_zero_uuids_return_one(self):
		#uuids = couch.uuids(0)
		#self.assertEqual(len(uuids), 1)

	#def test_get_minus_one_uuid(self):
		#uuids = couch.uuids(0)
		#self.assertEqual(len(uuids), 0)

	#def test_get_one_hundred_uuids(self):
		#uuids = couch.uuids(100)
		#self.assertEqual(len(uuids), 100)

	#def test_get_one_thousand_uuids(self):
		#uuids = couch.uuids(1000)
		#self.assertEqual(len(uuids), 1000)

	#def test_get_ten_thousand_uuids(self):
		#try:
			#uuids = couch.uuids(10000)
		#except couchdb.ServerError as e:
			#print e
			#status, message = e
			#self.assertEqual(status, 403)
			#self.assertEqual(403, 'forbidden')
        
class DbTestCase(unittest.TestCase):
	test_db_name = 'avancedb-test'

	def test_get_standard_databases(self):
		self.assertEqual(len(couch), 2)
		self.assertIsNotNone(couch['_replicator'])
		self.assertIsNotNone(couch['_users'])

	def test_shouldnt_find_db(self):
		self.assertFalse(self.test_db_name in couch)

if __name__ == "__main__":
    unittest.main() # run all tests
