from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

	
	def test_index(self):
		tester = app.test_client(self)
		response=tester.get('/login',content_type='html/text')
		self.assertEqual(response.status_code, 200)

	def test_login_page_loads(self):
		tester=app.test_client(self)
		response=tester.get('/login',content_type='html/text')
		self.assertTrue(b'Please login' in response.data)

	def test_correct_login(self):
		tester=app.test_client(self)
		response=tester.post('/login',
			data=dict(username='admin',
				password='admin'),follow_redirects=True)
		self.assertIn(b'You were just logged in',response.data)
	
	def test_incorrect_login(self):
		tester=app.test_client(self)
		response=tester.post('/login',
			data=dict(username='worng',
				password='wrong'),follow_redirects=True)
		self.assertIn(b'Invalid credendtials. Please try it again.',response.data)

	def test_logout(self):
		tester=app.test_client(self)
		tester.post('/login',
			data=dict(username='admin',
				password='admin'),follow_redirects=True)
		response=tester.get('/logout',follow_redirects=True)
		self.assertIn(b'You were just logged out!',response.data)

	#Ensure that the main page requires login
	def test_main_route_requires_login(self):
		tester=app.test_client(self)
		response=tester.get('/',follow_redirects=True)
		self.assertTrue(b'You need to login first.' in response.data)

	def test_main_route_requires_logout(self):
		tester=app.test_client(self)
		response=tester.get('/welcome',follow_redirects=True)
		print response
		self.assertTrue(b'Welcome to Flask'in response.data)

	def test_post_show_up(self):
		tester=app.test_client(self)
		response=tester.post('/login',
			data=dict(username='admin',
				password='admin'),follow_redirects=True)
		self.assertIn(b'You were just logged in',response.data)

if __name__=='__main__':
	unittest.main()