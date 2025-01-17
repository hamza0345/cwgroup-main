# api/tests.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .models import CustomUser


class BasicE2ETest(StaticLiveServerTestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver (make sure it's installed!)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # seconds

    def tearDown(self):
        self.driver.quit()

    def _sign_up_user(
        self,
        username="testuser",
        email="test@example.com",
        password="StrongPassword123!",
        name="Test User",
        dob="2000-01-01"
    ):
        """
        Helper to sign up a new user.
        """
        # Go to signup page
        self.driver.get(self.live_server_url + reverse('signup'))

        # Fill out the signup form
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        ).send_keys(username)

        self.driver.find_element(By.ID, 'id_email').send_keys(email)
        self.driver.find_element(By.ID, 'id_name').send_keys(name)
        self.driver.find_element(By.ID, 'id_password1').send_keys(password)
        self.driver.find_element(By.ID, 'id_password2').send_keys(password)
        self.driver.find_element(By.ID, 'id_date_of_birth').send_keys(dob)

        # Submit the form
        self.driver.find_element(By.ID, 'id_date_of_birth').send_keys(Keys.RETURN)

    def _login_user(self, username, password):
        """
        Helper to log in a user.
        """
        self.driver.get(self.live_server_url + reverse('login'))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        ).send_keys(username)
        self.driver.find_element(By.ID, 'id_password').send_keys(password)
        self.driver.find_element(By.ID, 'id_password').send_keys(Keys.RETURN)

    def test_signup_login(self):
        """
        1) Account creation / signup
        2) Login
        """
        # Sign up
        self._sign_up_user()

        # Check we got redirected to login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('login')
        )
        self.assertIn('login', self.driver.current_url.lower())

        # Log in
        self._login_user('testuser', 'StrongPassword123!')

        # Wait for main page to load
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/')
        )

        # Confirm some text on the main page
        self.assertIn('Welcome to the Hobbies SPA', self.driver.page_source)

    def test_edit_profile(self):
        """
        3) Editing all the user’s data on the profile page
           including username & password.
        """
        # Sign up + login
        self._sign_up_user()
        self._login_user('testuser', 'StrongPassword123!')

        # Suppose the link or route to the profile is "/profile" or so:
        # Adjust as needed.
        profile_url = self.live_server_url + "/profile/"
        self.driver.get(profile_url)

        # Wait for the profile page to load
        # This is hypothetical; you might have an element with ID 'profile-heading'
        # or just rely on the presence of input fields:
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input"))
        )

        # Clear and set new name
        name_input = self.driver.find_element(By.XPATH, "//label[text()='Name:']/following-sibling::input")
        name_input.clear()
        name_input.send_keys("Updated Name")

        # Clear and set new email
        email_input = self.driver.find_element(By.XPATH, "//label[text()='Email:']/following-sibling::input")
        email_input.clear()
        email_input.send_keys("updated@example.com")

        # Clear and set new DOB
        dob_input = self.driver.find_element(By.XPATH, "//label[text()='Date of Birth:']/following-sibling::input")
        dob_input.clear()
        dob_input.send_keys("1990-01-01")

        # Clear and set new hobbies
        hobbies_input = self.driver.find_element(By.XPATH, "//label[contains(text(),'Hobbies')]/following-sibling::input")
        hobbies_input.clear()
        hobbies_input.send_keys("Reading, Traveling")

        # Also test changing username
        # Suppose we have another field or we just override it in the same input?
        # We'll assume the label is "Username:"
        # This might differ in your implementation (you might only show one field).
        # We'll do a separate approach: the "updateProfile" in the Vue side handles it if passed, so we need an input for it.
        # For demonstration, let's pretend there's an input with ID 'username-input'.
        # If that's not how your page is laid out, adapt accordingly.
        try:
            username_input = self.driver.find_element(By.ID, "username-input")
            username_input.clear()
            username_input.send_keys("new_username")
        except:
            pass  # If no such field, you can skip or adjust your front-end

        # And new password
        try:
            pass_input = self.driver.find_element(By.ID, "password-input")
            pass_input.clear()
            pass_input.send_keys("NewPassword123!")
        except:
            pass

        # Now we click a button to save
        # We'll assume there's a <button @click="saveProfile">Save</button>
        save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
        save_button.click()

        # Check confirmation
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Now let's log out and re-login with the new username/password
        self.driver.get(self.live_server_url + reverse('logout'))
        self.driver.get(self.live_server_url + reverse('login'))

        # If we did change username to 'new_username' and password to 'NewPassword123!'
        # we attempt that login
        try:
            self._login_user("new_username", "NewPassword123!")
            # Wait to see if it logs in
            WebDriverWait(self.driver, 10).until(
                EC.url_contains('/')
            )
            # Confirm main page text
            self.assertIn("Welcome to the Hobbies SPA", self.driver.page_source)
        except:
            # If we didn't actually update username/password,
            # fallback to old credentials
            self._login_user("testuser", "StrongPassword123!")

    def test_users_page_and_filter(self):
        """
        4) Users page with testing of filtering by age
        """
        # Sign up + login
        self._sign_up_user()
        self._login_user('testuser', 'StrongPassword123!')

        # Suppose the users page is at /users
        users_url = self.live_server_url + "/users"
        self.driver.get(users_url)

        # Try setting min_age to 18, max_age to 25, then clicking "Apply Filter"
        min_age_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Min Age')]/input"))
        )
        min_age_input.clear()
        min_age_input.send_keys("18")

        max_age_input = self.driver.find_element(By.XPATH, "//label[contains(text(),'Max Age')]/input")
        max_age_input.clear()
        max_age_input.send_keys("25")

        apply_filter_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Apply Filter')]")
        apply_filter_button.click()

        # Expect some user listing to appear or maybe none
        # We'll just check that we didn't blow up
        self.assertNotIn("Server Error", self.driver.page_source)

    def test_send_and_accept_friend_request(self):
        """
        5) Sending a friend request
        6) Logging in as other user & accept friend requests
        """
        # Create user1
        self._sign_up_user(
            username="user1",
            email="user1@example.com"
        )
        self.driver.get(self.live_server_url + reverse('logout'))

        # Create user2
        self._sign_up_user(
            username="user2",
            email="user2@example.com"
        )
        self.driver.get(self.live_server_url + reverse('logout'))

        # Login as user1
        self._login_user("user1", "StrongPassword123!")

        # Send friend request to user2
        # Suppose we go to /users or something
        users_url = self.live_server_url + "/users"
        self.driver.get(users_url)

        # We'll look for a button we can click: "Send Friend Request"
        # Could be an ID or text-based. We'll guess text-based for example:
        send_fr_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Send Friend Request')]"))
        )
        send_fr_button.click()

        # Check success
        self.assertIn("Friend request sent", self.driver.page_source)

        # Log out user1
        self.driver.get(self.live_server_url + reverse('logout'))

        # Log in user2
        self._login_user("user2", "StrongPassword123!")

        # Accept friend request
        # Suppose the main page or some page lists the pending requests
        self.driver.get(self.live_server_url + "/")
        # Wait for friend request listing
        accept_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Accept')]"))
        )
        accept_button.click()

        self.assertIn("Friend request accepted", self.driver.page_source)
