from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestE2E(StaticLiveServerTestCase):
    """
    End-to-end tests for:
    1. Account creation
    2. Login
    3. Profile editing
    4. User filtering
    5. Sending and accepting friend requests
    """

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    # ---------------------------------------
    # Helper Methods
    # ---------------------------------------

    def go_to_url(self, url):
        self.driver.get(url)
        time.sleep(1)

    def fill_input(self, field_id, value):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        field.clear()
        field.send_keys(value)

    def click_button(self, xpath):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
        time.sleep(1)

    def sign_up_user(self, username, email, name, password, dob):
        self.go_to_url(self.live_server_url + reverse("signup"))
        self.fill_input("id_username", username)
        self.fill_input("id_email", email)
        self.fill_input("id_name", name)
        self.fill_input("id_password1", password)
        self.fill_input("id_password2", password)
        self.fill_input("id_date_of_birth", dob)
        self.click_button("//button[contains(text(),'Sign up')]")

    def login_user(self, username, password):
        self.go_to_url(self.live_server_url + reverse("login"))
        self.fill_input("id_username", username)
        self.fill_input("id_password", password)
        self.click_button("//button[contains(text(),'Login')]")
    
    def click_tab(self, tab_text):
        """Click on a navigation tab by its visible text."""
        tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//nav//a[contains(text(), '{tab_text}')]"))
        )
        tab.click()
        time.sleep(1)  # Allow time for the transition


    # ---------------------------------------
    # Tests
    # ---------------------------------------

    def test_1_signup_and_login(self):
        """
        Test account creation and login.
        """
        # Sign up a new user
        self.sign_up_user("testuser", "test@example.com", "Test User", "SecurePass123!", "2000-01-01")

        # Verify redirect to login page
        self.assertIn("login", self.driver.current_url)

        # Log in
        self.login_user("testuser", "SecurePass123!")

        # Verify successful login and redirection
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Welcome')]"))
        )
        self.assertIn("Welcome to the Hobbies SPA", self.driver.page_source)

    # def test_2_edit_profile(self):
    #     """
    #     Test editing user profile details using the profile tab navigation.
    #     """
    #     # Sign up and log in the user
    #     self.sign_up_user("testuser", "test@example.com", "Test User", "SecurePass123!", "2000-01-01")
    #     self.login_user("testuser", "SecurePass123!")

    #     # Wait for navigation bar to be clickable and click the Profile tab
    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//nav//a[contains(text(),'Profile')]"))
    #     ).click()

    #     # Wait explicitly for the profile page to load by checking for a unique element
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Profile')]"))
    #     )

    #     # Edit profile details
    #     self.fill_input("id_name", "Updated User")
    #     self.fill_input("id_email", "updated@example.com")
    #     self.fill_input("id_date_of_birth", "1995-12-25")
    #     self.fill_input("id_hobbies", "Reading, Coding")

    #     # Save profile changes
    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Save')]"))
    #     ).click()

    #     # Verify success message
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Profile updated successfully')]"))
    #     )
    #     self.assertIn("Profile updated successfully", self.driver.page_source)




    # # def test_3_users_page_filter(self):
    # #     """
    # #     Test filtering users by age on the users page.
    # #     """
    # #     self.sign_up_user("testuser1", "user1@example.com", "User One", "SecurePass123!", "2000-01-01")
    # #     self.sign_up_user("testuser2", "user2@example.com", "User Two", "SecurePass123!", "1995-05-15")
    #     self.login_user("testuser1", "SecurePass123!")

    #     # Navigate to users page
    #     self.go_to_url(self.live_server_url + "/users/")

    #     # Apply age filters
    #     self.fill_input("min-age", "20")
    #     self.fill_input("max-age", "30")
    #     self.click_button("//button[contains(text(),'Apply Filter')]")

    #     # Verify filtered users are displayed
    #     self.assertNotIn("Server Error", self.driver.page_source)

    # def test_4_send_and_accept_friend_request(self):
    #     """
    #     Test sending and accepting a friend request.
    #     """
    #     # Sign up two users
    #     self.sign_up_user("user1", "user1@example.com", "User One", "SecurePass123!", "2000-01-01")
    #     self.sign_up_user("user2", "user2@example.com", "User Two", "SecurePass123!", "1995-05-15")

    #     # User1 sends a friend request to User2
    #     self.login_user("user1", "SecurePass123!")
    #     self.go_to_url(self.live_server_url + "/users/")
    #     self.click_button("//button[contains(text(),'Send Friend Request')]")
    #     self.assertIn("Friend request sent", self.driver.page_source)
    #     self.go_to_url(self.live_server_url + reverse("logout"))

    #     # User2 logs in and accepts the request
    #     self.login_user("user2", "SecurePass123!")
    #     self.go_to_url(self.live_server_url + "/")
    #     self.click_button("//button[contains(text(),'Accept')]")
    #     self.assertIn("Friend request accepted", self.driver.page_source)
