from authentication.models import UserProfile
from base import mods
from base.tests import BaseTestCase
from django.contrib import auth
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver


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
        self.assertTrue(driver.find_element_by_xpath("//div[@id='popupadmin']/h4").is_displayed())
        self.assertTrue(driver.find_element_by_id("username").is_displayed())
        self.assertTrue(driver.find_element_by_id("password").is_displayed())
        self.assertTrue(driver.find_element_by_xpath("//button[@type='submit']").is_displayed())
        self.assertTrue(driver.find_element_by_xpath("(//button[@id='signIn'])[2]").is_displayed())
        driver.close()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
