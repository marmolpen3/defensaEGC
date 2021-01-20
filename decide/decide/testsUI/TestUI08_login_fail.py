from authentication.models import UserProfile
from base import mods
from base.tests import BaseTestCase
from django.contrib import auth
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AppDynamicsJob(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/')
        driver.set_window_size(1386, 692)
        driver.find_element_by_id("btn-abrir-popup").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("UserLoginFailed")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("iemrgoierm")
        driver.find_element_by_id("password").send_keys(Keys.ENTER)
        self.assertEquals(len(driver.find_elements_by_id("welcomeID")), 0)
        driver.close()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()  
