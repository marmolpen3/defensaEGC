import time

from authentication.models import UserProfile
from base import mods
from base.tests import BaseTestCase
from django.contrib import auth
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestSuccess(StaticLiveServerTestCase):
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
        self.driver.find_element(By.ID, "signIn").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").send_keys("prueba10")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("prueba10@gmail.com")
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__18 .custom-control:nth-child(1) > .custom-control-label").click()
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__21 .custom-control:nth-child(1) > .custom-control-label").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").send_keys("prueba10")
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.switch_to.alert.accept()
        self.driver.find_element(By.ID, "btn-abrir-popup").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("prueba10")
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__12 > div").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("prueba10")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        assert self.driver.find_element(By.ID, "welcomeID").text == "Welcome"
        assert self.driver.find_element(By.CSS_SELECTOR, "strong:nth-child(2)").text == "prueba10!"
        driver.close()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
