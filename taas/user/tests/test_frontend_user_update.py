from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from taas.user.tests.factories import UserFactory


class UserUpdateTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserUpdateTest, cls).setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UserUpdateTest, cls).tearDownClass()

    def test_logged_in_user_can_access_update_page(self):
        self.go_to_update_page()

    def test_logged_in_user_can_update_his_first_name(self):
        self.go_to_update_page()

        first_name = self.selenium.find_element_by_id('id_first_name')
        first_name.clear()
        first_name.send_keys("Test")

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//ul/li[text() = "Information has been updated."]'))
        self.assertTrue(self.selenium.find_element_by_xpath('//input[@value="Test"]'))

    def test_logged_in_user_can_update_his_last_name(self):
        self.go_to_update_page()

        last_name = self.selenium.find_element_by_id('id_last_name')
        last_name.clear()
        last_name.send_keys("Test")

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//ul/li[text() = "Information has been updated."]'))
        self.assertTrue(self.selenium.find_element_by_xpath('//input[@value="Test"]'))

    def test_logged_in_user_can_update_his_phone_number(self):
        self.go_to_update_page()

        phone_number = self.selenium.find_element_by_id('id_phone_number')
        phone_number.clear()
        phone_number.send_keys("59284829")

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//ul/li[text() = "Information has been updated."]'))
        self.assertTrue(self.selenium.find_element_by_xpath('//input[@value="59284829"]'))

    def test_logged_in_user_can_update_his_password_with_valid_parameters(self):
        self.go_to_update_page()
        self.selenium.find_element_by_id('id_change_password').click()

        self.selenium.find_element_by_id('id_old_password').send_keys('isherenow')
        self.selenium.find_element_by_id('id_new_password1').send_keys('testisherenow')
        self.selenium.find_element_by_id('id_new_password2').send_keys('testisherenow')

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//ul/li[text() = "Information has been updated."]'))

    def test_logged_in_user_cannot_update_his_password_with_invalid_old_password(self):
        self.go_to_update_page()
        self.selenium.find_element_by_id('id_change_password').click()

        self.selenium.find_element_by_id('id_old_password').send_keys('isnothere')
        self.selenium.find_element_by_id('id_new_password1').send_keys('testisherenow')
        self.selenium.find_element_by_id('id_new_password2').send_keys('testisherenow')

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//p[text() = "Your old password was entered incorrectly. Please enter it again."]'))

    def test_logged_in_user_cannot_update_his_password_to_too_short_password(self):
        self.go_to_update_page()
        self.selenium.find_element_by_id('id_change_password').click()

        self.selenium.find_element_by_id('id_old_password').send_keys('isnothere')
        self.selenium.find_element_by_id('id_new_password1').send_keys('test')
        self.selenium.find_element_by_id('id_new_password2').send_keys('test')

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//p[contains(text(), "Ensure this value has at least 8 characters")]'))

    def test_logged_in_user_cannot_update_his_password_with_not_matching_new_passwords(self):
        self.go_to_update_page()
        self.selenium.find_element_by_id('id_change_password').click()

        self.selenium.find_element_by_id('id_old_password').send_keys('isherenow')
        self.selenium.find_element_by_id('id_new_password1').send_keys('testisherenow2')
        self.selenium.find_element_by_id('id_new_password2').send_keys('testisherenow')

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//p[text() = "The two new password fields didn\'t match."]'))

    def test_logged_in_user_cannot_update_his_password_without_first_new_password(self):
        self.go_to_update_page()
        self.selenium.find_element_by_id('id_change_password').click()

        self.selenium.find_element_by_id('id_old_password').send_keys('isherenow')
        self.selenium.find_element_by_id('id_new_password2').send_keys('testisherenow')

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//p[text() = "New password is required."]'))

    def test_logged_in_user_cannot_update_his_password_without_second_new_password(self):
        self.go_to_update_page()
        self.selenium.find_element_by_id('id_change_password').click()

        self.selenium.find_element_by_id('id_old_password').send_keys('isherenow')
        self.selenium.find_element_by_id('id_new_password1').send_keys('testisherenow')

        self.selenium.find_element_by_id('submit-button').click()
        self.assertIn("User modification", self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_xpath(
            '//p[text() = "New password confirmation is required."]'))

    def login_user(self):
        self.user = UserFactory(is_active=True)
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.assertIn("Tartu Agility Playground", self.selenium.title)
        self.selenium.find_element_by_xpath('//*[@id="innerwrap"]/header/div[3]/ul/li[1]/a').click()
        self.selenium.find_element_by_id('id_username').send_keys(self.user.email)
        self.selenium.find_element_by_id('id_password').send_keys('isherenow')
        self.selenium.find_element_by_xpath('//input[@value="Login"]').click()
        self.assertIn('Tartu Agility Playground', self.selenium.title)

    def go_to_update_page(self):
        self.login_user()
        self.selenium.find_element_by_xpath('//*[@id="innerwrap"]/ul/li[4]/a').click()
        self.assertIn('User modification', self.selenium.title)


class UserDeactivationTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserDeactivationTest, cls).setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UserDeactivationTest, cls).tearDownClass()

    def test_logged_in_user_can_access_deactivation_page(self):
        self.go_to_update_page()
        self.selenium.find_element_by_xpath('//input[@value="Deactivate"]').click()
        self.assertTrue(self.selenium.find_element_by_xpath('//h1[text() = "Deactivate account"]'))

    def test_logged_in_user_can_deactivate_his_account(self):
        self.go_to_update_page()
        self.selenium.find_element_by_xpath('//input[@value="Deactivate"]').click()

        self.assertTrue(self.selenium.find_element_by_xpath('//h1[text() = "Deactivate account"]'))
        self.selenium.find_element_by_id("id_password").send_keys('isherenow')
        self.selenium.find_element_by_xpath('//input[@value="Deactivate"]').click()

        self.assertIn('Tartu Agility Playground', self.selenium.title)
        self.selenium.find_element_by_xpath(
            '//ul/li[text() = "User has been deactivated."]')

    def login_user(self):
        self.user = UserFactory(is_active=True)
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.assertIn("Tartu Agility Playground", self.selenium.title)
        self.selenium.find_element_by_xpath('//*[@id="innerwrap"]/header/div[3]/ul/li[1]/a').click()
        self.selenium.find_element_by_id('id_username').send_keys(self.user.email)
        self.selenium.find_element_by_id('id_password').send_keys('isherenow')
        self.selenium.find_element_by_xpath('//input[@value="Login"]').click()
        self.assertIn('Tartu Agility Playground', self.selenium.title)

    def go_to_update_page(self):
        self.login_user()
        self.selenium.find_element_by_xpath('//*[@id="innerwrap"]/ul/li[4]/a').click()
        self.assertIn('User modification', self.selenium.title)
