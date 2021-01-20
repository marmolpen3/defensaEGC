from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from booth.tests import BoothTests
from voting.models import Voting, Question, QuestionOption
from census.models import Census
from django.utils import timezone
from django.conf import settings
from mixnet.models import Auth
from authentication.models import UserProfile

from base import mods
import time

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE LOGIN-----------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class LoginInterfaceTests(StaticLiveServerTestCase):
    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    def test_interface_login_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element_by_id('username').send_keys("voter1")
        self.driver.find_element_by_id('password').send_keys("123",Keys.ENTER)

        #Cuando el login es correcto, se redirige a la página de dashboard
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')

    def test_interface_login_fail(self):
        #Se loguea con un usuario inexistente
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element_by_id('username').send_keys("badvoter1")
        self.driver.find_element_by_id('password').send_keys("badpass1",Keys.ENTER)

        #Cuando el login es incorrecto, se mantiene en la página y aparece una alerta
        alert = self.driver.find_element_by_id('loginFail')
        self.assertEquals(alert.text,'El usuario no está registrado en el sistema.')
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE SUGGESTING------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class SuggestingInterfaceTests(StaticLiveServerTestCase):

    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    def test_interface_create_suggestion_fail_date_before_now(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element_by_id("suggestingTitle").send_keys("test1")
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("04")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2020")
        self.driver.find_element_by_id("suggestingContent").send_keys("test1")
        self.driver.find_element_by_id("submitSugForm").click()

        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

    def test_interface_create_suggestion_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element_by_id("suggestingTitle").send_keys("test1")
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2022")
        self.driver.find_element_by_id("suggestingContent").send_keys("test1")
        self.driver.find_element_by_id("submitSugForm").click()

        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')

    def test_interface_create_suggestion_fail_empty_suggestingTitle(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("04")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2022")
        self.driver.find_element(By.ID, "suggestingContent").send_keys("test1")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

    def test_interface_create_suggestion_fail_empty_suggestingDate(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element(By.ID, "suggestingTitle").send_keys("test1")
        self.driver.find_element(By.ID, "suggestingContent").send_keys("test1")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

    def test_interface_create_suggestion_fail_empty_suggestingContent(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element(By.ID, "suggestingTitle").send_keys("test1")
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("04")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2022")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE ACCESIBILIDAD---------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class AccesibilityInterfaceTests(StaticLiveServerTestCase):
    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    def test_accesibility_dalt_deutera_protan_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.XPATH, "//*[@role='button']").click()
        vis_types = self.driver.find_elements(By.XPATH, "//*[@role='menuitem']")
        vis_types[0].click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()

        form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        self.assertEquals(form_radios_uniq[0].value_of_css_property('background-color'),'rgba(82, 172, 255, 1)')

    def test_accesibility_dalt_tritan_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.XPATH, "//*[@role='button']").click()
        vis_types = self.driver.find_elements(By.XPATH, "//*[@role='menuitem']")
        vis_types[1].click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()

        form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        self.assertEquals(form_radios_uniq[0].value_of_css_property('background-color'),'rgba(255, 102, 102, 1)')

    def test_accesibility_dalt_normal_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.XPATH, "//*[@role='button']").click()
        vis_types = self.driver.find_elements(By.XPATH, "//*[@role='menuitem']")
        vis_types[2].click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()

        form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        self.assertEquals(form_radios_uniq[0].value_of_css_property('background-color'),'rgba(108, 117, 125, 1)')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE CABINA----------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class BoothInterfaceTests(StaticLiveServerTestCase):
    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        u = UserProfile(id=1, username='voter1', sex='M')
        u.set_password('123')
        u.save()
        token= mods.post('authentication', entry_point='/login/', json={'username':'voter1', 'password': '123'})
        # Add session token
        session = self.client.session
        session['user_token'] = token
        session.save()

        q2 = Question(id=2,desc='Multiple option question', option_types=2)
        q2.save()
        for i in range(4):
            opt = QuestionOption(question=q2, option='option {}'.format(i+1))
            opt.save()

       
        q3 = Question(id=3,desc='Rank order scale question', option_types=3)
        q3.save()
        for i in range(5):
            opt = QuestionOption(question=q3, option='option {}'.format(i+1))
            opt.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,defaults={'me':True,'name':'base'})
        a.save()
        v2 = Voting(id=2, name='Rank question voting',desc='Rank question voting...', points=1, start_date=timezone.now())
        v2.save()
        v2.question.add(q3)
        v3 = Voting(id=3, name='Multiple question voting',desc='Multiple question voting...', points=1, start_date=timezone.now())
        v3.save()
        v3.question.add(q2)

        v2.auths.add(a)
        Voting.create_pubkey(v2)
        #Add user to census
        census = Census(voting_id=v2.id, voter_id=u.id)
        census.save()
        
        v3.auths.add(a)
        Voting.create_pubkey(v3)
        #Add user to census
        census = Census(voting_id=v3.id, voter_id=u.id)
        census.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()


    def test_booth_voting_unique_no_option_selected(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
        self.driver.find_element(By.LINK_TEXT, "Enviar").click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/1/1/')


    def test_booth_voting_multiple_no_option_selected(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "Multiple question voting").click()
        self.driver.find_element(By.LINK_TEXT, "Enviar").click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/3/2/')


    def test_booth_voting_rank_no_option_selected(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.LINK_TEXT, "Rank question voting").click()
        rankButton = self.driver.find_elements(By.ID, "rankSendButton")
        self.assertTrue(len(rankButton)<1)
