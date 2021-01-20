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
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        driver.find_element_by_xpath("//div[@id='app-decide']/div[2]/div/div/h2").click()
        self.assertEqual("Help with voice assistants", driver.find_element_by_xpath("//div[@id='app-decide']/div[2]/div/div/h2").text)
        driver.find_element_by_xpath("//div[@id='app-decide']/nav/a/img").click()
        driver.find_element_by_id("welcome").click()
        self.assertEqual("Welcome to Decide, an online voting platform. This is the main page. Here, you can login to your account and press booth to vote or press visualizer to see the results.", driver.find_element_by_id("welcome").text)
        driver.close()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
