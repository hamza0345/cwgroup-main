from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestE2E(StaticLiveServerTestCase):
    """
    End-to-end tests for:
    1. Account creation and login
    3. Profile editing
    4. User filtering
    5. Sending and accepting friend requests
    """

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    # Helper Methods
    def go_to_url(self, url):
        """Navigate to a specific URL."""
        self.driver.get(url)
        time.sleep(1)

    def fill_input(self, field_id, value):
        """Fill input fields by their ID (for SSR forms)."""
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        field.clear()
        field.send_keys(value)

    def fill_input_by_xpath(self, label_text, value):
        """Fill input fields on Vue pages using label text."""
        xpath = f"//label[contains(text(),'{label_text}')]/input"
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        field.clear()
        field.send_keys(value)

    def click_button(self, xpath):
        """Click a button using XPath."""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
        time.sleep(1)

    def click_tab(self, tab_text):
        """Click a tab in the navigation bar by its visible text."""
        tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//nav//a[contains(text(),'{tab_text}')]"))
        )
        tab.click()
        time.sleep(1)

    def sign_up_user(self, username, email, name, password, dob):
        """Perform account creation."""
        self.go_to_url(self.live_server_url + reverse("signup"))
        self.fill_input("id_username", username)
        self.fill_input("id_email", email)
        self.fill_input("id_name", name)
        self.fill_input("id_password1", password)
        self.fill_input("id_password2", password)
        self.fill_input("id_date_of_birth", dob)
        self.click_button("//button[contains(text(),'Sign up')]")

    def login_user(self, username, password):
        """Perform user login."""
        self.go_to_url(self.live_server_url + reverse("login"))
        self.fill_input("id_username", username)
        self.fill_input("id_password", password)
        self.click_button("//button[contains(text(),'Login')]")

    # Tests
    def test_1_signup_and_login(self):
        """
        Test account creation and login.
        """
        # Signs up a new user
        self.sign_up_user("testuser", "test@example.com", "Test User", "SecurePass123!", "2000-01-01")

        # Verify redirect to login page
        self.assertIn("login", self.driver.current_url)

        # Log in
        self.login_user("testuser", "SecurePass123!")

        # Verify successful login by checking for a welcome message
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Welcome')]"))
        )
        self.assertIn("Welcome to the Hobbies SPA", self.driver.page_source)

    def test_2_edit_profile(self):
        """
        Test editing user profile details via Profile tab.
        """
        # Sign up & log in
        self.sign_up_user("testuser", "test@example.com", "Test User", "SecurePass123!", "2000-01-01")
        self.login_user("testuser", "SecurePass123!")

        # Navigate to Profile tab
        self.click_button('//a[contains(text(),"Profile")]')

        # Edit profile details
        self.fill_input_by_xpath("Name:", "Updated User")
        self.fill_input_by_xpath("Email:", "updated@example.com")
        self.fill_input_by_xpath("Date of Birth:", "12-12-1990")
        # self.fill_input_by_xpath("Hobbies (comma-separated):", "Reading, Hiking")

        # Save changes
        self.click_button("//button[contains(text(),'Save')]")

        # Verify success alert
        alert_text = self.driver.switch_to.alert
        self.assertIn("Profile updated successfully!", alert_text.text)
        alert_text.accept()

    def test_3_users_page_filter(self):
        """
        Test filtering users by age.
        """
        # Create two users
        self.sign_up_user("testuser1", "user1@example.com", "User One", "SecurePass123!", "10-10-2000")
        self.sign_up_user("testuser2", "user2@example.com", "User Two", "SecurePass123!", "15-11-1996")

        # Log in as the first user
        self.login_user("testuser1", "SecurePass123!")

        # Navigate to Users tab
        self.click_button('//a[contains(text(),"Users")]')

        # Filter users by age
        self.fill_input_by_xpath("Min Age:", "20")
        self.fill_input_by_xpath("Max Age:", "30")
        self.click_button("//button[contains(text(),'Apply Filter')]")

        # Verify results are filtered
        self.assertNotIn("Server Error", self.driver.page_source)

    def test_4_send_and_accept_friend_request(self):
        """
        Test sending and accepting a friend request.
        """
        # Sign up two users
        self.sign_up_user("testuser1", "user1@example.com", "User One", "SecurePass123!", "10-10-2000")
        self.sign_up_user("testuser2", "user2@example.com", "User Two", "SecurePass123!", "15-11-1996")

        # User1 logs in and sends a friend request
        self.login_user("testuser1", "SecurePass123!")
        self.click_button('//a[contains(text(),"Users")]')
        self.click_button("//button[contains(text(),'Send Friend Request')]")

        # Verify request sent alert
        alert_text = self.driver.switch_to.alert
        self.assertIn("Friend request sent!", alert_text.text)
        alert_text.accept()

        # User2 logs in and accepts the request
        self.login_user("testuser2", "SecurePass123!")
        self.click_button('//a[contains(text(),"Main")]')
        self.click_button("//button[contains(text(),'Accept')]")

        # Verify request accepted alert
        alert_text = self.driver.switch_to.alert
        self.assertIn("Friend request accepted", alert_text.text)
        alert_text.accept()
