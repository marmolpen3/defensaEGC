import time

from authentication.models import UserProfile
from base import mods
from base.tests import BaseTestCase
from django.contrib import auth
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class AppDynamicsJob(StaticLiveServerTestCase):
  def setUp(self):
      self.base = BaseTestCase()
      self.base.setUp()

      options = webdriver.ChromeOptions()
      options.headless = True
      self.driver = webdriver.Chrome(options=options)

      super().setUp()

  def tearDown(self):
      super().tearDown()
      self.driver.quit()

      self.base.tearDown()  

  def test_fail(self):
    driver = self.driver
    driver.get(f'{self.live_server_url}/')
    driver.set_window_size(1386, 692)
    self.driver.find_element(By.ID, "signIn").click()
    self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").click()
    self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").send_keys("admin")
    self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__18 .custom-control:nth-child(1) > .custom-control-label").click()
    self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__21 .custom-control:nth-child(1) > .custom-control-label").click()
    self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").click()
    self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").send_keys("qwerty12")
    self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(7)").click()
    time.sleep(2)
    assert self.driver.find_element(By.CSS_SELECTOR, ".alert").text != "×\\\\nError: Bad Request"
  
