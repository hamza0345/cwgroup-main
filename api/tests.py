from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse


class BasicE2ETest(StaticLiveServerTestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
        self.driver.implicitly_wait(10)  # Implicit wait for element loading

    def tearDown(self):
        # Quit the WebDriver after each test
        self.driver.quit()

    def test_signup_login(self):
        # Go to the signup page
        self.driver.get(self.live_server_url + reverse('signup'))

        # Fill out the signup form
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input.send_keys('testuser')  # Username

        email_input = self.driver.find_element(By.ID, 'id_email')
        email_input.send_keys('test@example.com')  # Email address

        name_input = self.driver.find_element(By.ID, 'id_name')
        name_input.send_keys('Test User')  # Name

        password_input = self.driver.find_element(By.ID, 'id_password1')  # Correct ID for password1
        password_input.send_keys('StrongPassword123!')  # Password

        password_confirm_input = self.driver.find_element(By.ID, 'id_password2')  # Correct ID for password2
        password_confirm_input.send_keys('StrongPassword123!')  # Password confirmation

        dob_input = self.driver.find_element(By.ID, 'id_date_of_birth')  # Correct ID for date_of_birth
        dob_input.send_keys('2000-01-01')  # Example date in YYYY-MM-DD format

        # Submit the form
        dob_input.send_keys(Keys.RETURN)

        # Wait for the page to load and check if redirected to login page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('login')
        )

        # Assert that we are on the login page
        self.assertIn('login', self.driver.current_url.lower())

        # Log in with the newly created account
        username_input = self.driver.find_element(By.ID, 'id_username')
        password_input = self.driver.find_element(By.ID, 'id_password')
        username_input.send_keys('testuser')
        password_input.send_keys('StrongPassword123!')
        password_input.send_keys(Keys.RETURN)

        # Wait for the page to load and check if redirected to the main SPA
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/')
        )

        # Check if redirected to the main SPA
        self.assertIn(self.live_server_url + '/', self.driver.current_url)

        # Check for a successful login message or element
        self.assertIn('Welcome', self.driver.page_source)  # Adjust based on your app's content

        # Additional debugging: Check for any error messages
        if 'Invalid credentials' in self.driver.page_source:
            print("Login failed: Invalid credentials")
        elif 'Please correct the errors below' in self.driver.page_source:
            print("Login failed: Form validation errors")

    def test_edit_profile(self):
        # Log in before editing the profile
        self.test_signup_login()
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
        self.driver.find_element(By.ID, 'submit').click()  # Adjust the ID if necessary

        # Check if the profile was updated successfully
        self.assertIn('Profile updated', self.driver.page_source)  # Adjust based on your app's content

    def test_send_friend_request(self):
        # Log in and navigate to the users page
        self.test_signup_login()
        self.driver.get(self.live_server_url + reverse('users'))  # Adjust the URL name as needed

        # Click the "Send Friend Request" button
        self.driver.find_element(By.ID, 'send_friend_request_1').click()  # Adjust the ID for the button
        self.assertIn('Friend request sent', self.driver.page_source)  # Adjust based on your app's content

    def test_accept_friend_request(self):
        # Send a friend request first
        self.test_send_friend_request()
        self.driver.get(self.live_server_url + reverse('friend_requests'))  # Adjust the URL name as needed

        # Accept the friend request
        self.driver.find_element(By.ID, 'accept_request_1').click()  # Adjust the ID for the button
        self.assertIn('Friend request accepted', self.driver.page_source)  # Adjust based on your app's content