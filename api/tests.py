from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

class BasicE2ETest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_signup_login(self):
        # Go to signup page
        self.driver.get(self.live_server_url + reverse('signup'))
        
        # Fill out the signup form
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys('testuser')
        name_input = self.driver.find_element(By.ID, 'id_name')
        name_input.send_keys('Test User')
        email_input = self.driver.find_element(By.ID, 'id_email')
        email_input.send_keys('test@example.com')
        pwd_input = self.driver.find_element(By.ID, 'id_password')
        pwd_input.send_keys('mypassword')
        pwd_input.send_keys(Keys.RETURN)

        # Check if redirected to login page
        self.assertIn('login', self.driver.current_url.lower())

        # Now login
        username_input = self.driver.find_element(By.ID, 'id_username')
        password_input = self.driver.find_element(By.ID, 'id_password')
        username_input.send_keys('testuser')
        password_input.send_keys('mypassword')
        password_input.send_keys(Keys.RETURN)

        # Check if redirected to main SPA
        self.assertIn(self.live_server_url + '/', self.driver.current_url)
        self.assertIn('Welcome', self.driver.page_source)  # Adjust based on your app's content

    def test_edit_profile(self):
        self.test_signup_login()  # Log in first
        self.driver.get(self.live_server_url + reverse('profile'))  # Adjust the URL name as needed

        # Fill out the profile edit form
        name_input = self.driver.find_element(By.ID, 'id_name')
        name_input.clear()  # Clear existing name
        name_input.send_keys('Updated User')

        email_input = self.driver.find_element(By.ID, 'id_email')
        email_input.clear()  # Clear existing email
        email_input.send_keys('updated@example.com')

        hobbies_input = self.driver.find_element(By.ID, 'id_hobbies')
        hobbies_input.clear()  # Clear existing hobbies
        hobbies_input.send_keys('Reading, Traveling')

        # Submit the form
        self.driver.find_element(By.ID, 'submit').click()  # Adjust the ID as needed

        # Check if the profile was updated
        self.assertIn('Profile updated', self.driver.page_source)  # Adjust based on your app's content
