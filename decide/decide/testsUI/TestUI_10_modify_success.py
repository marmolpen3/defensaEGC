# -*- coding: utf-8 -*-
import re
import time
import unittest

from authentication.models import UserProfile
from base.tests import BaseTestCase
from django.contrib import auth
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.common.exceptions import (NoAlertPresentException,
                                        NoSuchElementException)


class AppDynamicsJob(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = False
        user = UserProfile(username='test', sex='M', style='N', is_staff=False, is_superuser=False, is_active=True)
        user.set_password('test')
        user.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}')
        driver.find_element_by_id("btn-abrir-popup").click()
        driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("test")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("test")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Modify").click()
        driver.find_element_by_id("input-1").click()
        driver.find_element_by_id("input-1").clear()
        driver.find_element_by_id("input-1").send_keys("test2")
        driver.find_element_by_id("input-2").click()
        driver.find_element_by_id("input-2").clear()
        driver.find_element_by_id("input-2").send_keys("testModify@gmail.com")
        driver.find_element_by_xpath(
            "//fieldset[@id='__BVID__18']/div/div/label").click()
        driver.find_element_by_xpath(
            "//fieldset[@id='__BVID__23']/div/div/label").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("Profile data updated successfully.",
                         self.close_alert_and_get_its_text())

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
