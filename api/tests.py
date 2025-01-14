# from django.test import LiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from django.urls import reverse
# from .models import CustomUser

# class BasicE2ETest(StaticLiveServerTestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()  # or Firefox() if you prefer
#         self.driver.implicitly_wait(10)

#     def tearDown(self):
#         self.driver.quit()

#     def test_signup_login(self):
#         # Go to signup page
#         self.driver.get(self.live_server_url + '/signup/')
#         username_input = self.driver.find_element(By.ID, 'id_username')
#         username_input.send_keys('testuser')
#         name_input = self.driver.find_element(By.ID, 'id_name')
#         name_input.send_keys('Test User')
#         email_input = self.driver.find_element(By.ID, 'id_email')
#         email_input.send_keys('test@example.com')
#         pwd_input = self.driver.find_element(By.ID, 'id_password')
#         pwd_input.send_keys('mypassword')
#         pwd_input.send_keys(Keys.RETURN)

#         # Should redirect to login
#         self.assertIn('login', self.driver.current_url.lower())

#         # Now login
#         username_input = self.driver.find_element(By.ID, 'id_username')
#         password_input = self.driver.find_element(By.ID, 'id_password')
#         username_input.send_keys('testuser')
#         password_input.send_keys('mypassword')
#         password_input.send_keys(Keys.RETURN)

#         # Should redirect to main SPA
#         self.assertIn(self.live_server_url + '/', self.driver.current_url)

#         # Potentially check if the Vue app loaded
#         # e.g. check an element or the page title
#         # This is just a minimal example.

#     # Additional E2E tests for profile editing, sending friend requests, etc.
