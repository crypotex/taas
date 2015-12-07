import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from taas.user.tests.factories import UserFactory


os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = "localhost:8000-8010,8080,9200-9300"


class UserRegistrationTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserRegistrationTest, cls).setUpClass()
        cls.form_data = UserFactory.get_form_data()
        username = os.environ["SAUCE_USERNAME"]
        access_key = os.environ["SAUCE_ACCESS_KEY"]
        capabilities = {
            "tunnel-identifier": os.environ["TRAVIS_JOB_NUMBER"],
            "build": os.environ["TRAVIS_BUILD_NUMBER"],
            "tags": [os.environ["TRAVIS_PYTHON_VERSION"], "CI"]
        }
        hub_url = "%s:%s@localhost:4445" % (username, access_key)
        cls.selenium = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s/wd/hub" % hub_url)
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UserRegistrationTest, cls).tearDownClass()

    def test_user_can_access_registration(self):
        self.go_to_registration()

    def test_user_can_register_with_valid_data(self):
        self.go_to_registration()
        self.fill_the_registration_fields()

        self.selenium.find_element_by_id("terms").click()
        self.selenium.find_element_by_class_name("form").submit()
        self.assertIn("Tartu Agility Playground", self.selenium.title)
        self.selenium.find_element_by_xpath(
            '//ul/li[text() = "User has been successfully registered."]')

    def test_user_cannot_register_with_short_password(self):
        self.go_to_registration()

        self.form_data['password1'] = " "
        self.form_data['password2'] = " "
        self.fill_the_registration_fields()

        self.selenium.find_element_by_id("terms").click()
        self.selenium.find_element_by_class_name("form").submit()
        self.selenium.find_element_by_xpath('//p[contains(text(), "Ensure this value has at least 8 characters")]')

    def test_user_cannot_register(self):
        self.go_to_registration()

        self.form_data['last_name'] = ''
        self.form_data['password2'] = 'invalidpassword'
        self.fill_the_registration_fields()

        self.selenium.find_element_by_id("terms").click()
        self.selenium.find_element_by_class_name("form").submit()

        # Find if any fields were not filled in
        self.selenium.find_element_by_xpath('//p[text() = "This field is required."]')
        # Find if passwords did not match
        self.selenium.find_element_by_xpath('//p[text() = "The two password fields didn\'t match."]')

    def go_to_registration(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/"))

        element = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "en")))
        element.click()

        self.assertIn("Tartu Agility Playground", self.selenium.title)
        if self.selenium.find_element_by_xpath('//*[@id="desktop"]'):
            self.selenium.find_element_by_xpath('//*[@id="user-nav"]/ul/li[2]/a').click()
            self.assertIn("Registration", self.selenium.title)
        else:
            self.selenium.find_element_by_xpath('//*[@id="menu-button"]').click()
            self.selenium.find_element_by_xpath('//*[@id="cssmenu"]/ul/li[2]/a').click()
            self.assertIn("Registration", self.selenium.title)

    def fill_the_registration_fields(self):
        first_name = self.selenium.find_element_by_id("id_first_name")
        first_name.send_keys(self.form_data.get('first_name'))
        last_name = self.selenium.find_element_by_id("id_last_name")
        last_name.send_keys(self.form_data.get('last_name'))
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys(self.form_data.get('email'))
        phone_number = self.selenium.find_element_by_id("id_phone_number")
        phone_number.send_keys(self.form_data.get('phone_number'))
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys(self.form_data.get('password1'))
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys(self.form_data.get('password2'))
