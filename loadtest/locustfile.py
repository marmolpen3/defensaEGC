import json

from random import choice, randint

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost:8000"
VOTING = 1

class DefLogin(TaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))
        
    @task
    def index(self):
        self.client.get("/")
    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    def on_quit(self):
        self.voter = None

class DefHelpVoiceAssistant(TaskSet):

    @task
    def index(self):
        self.client.get("/")

    @task
    def HVA(self):
        self.client.get("/helpvoiceassistant/")

class DefLogOut(TaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))
        
    @task
    def index(self):
        self.client.get("/")
    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def getLogout(self):
        self.token= self.client.post("/authentication/logout/", self.token).json()

    def on_quit(self):
        self.voter = None


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))



class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/store/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING
        }), headers=headers)


    def on_quit(self):
        self.voter = None


class DefPostproc(SequentialTaskSet):

    def on_start(self):
        with open('votings.json') as f:
            self.votings = json.loads(f.read())
            self.voting = choice(list(self.votings.items()))

    @task
    def do_postproc(self):
        voting, json = self.voting
        self.client.post('/postproc/', json=json)

    def on_quit(self):
        self.voting = None


class Login(HttpUser):
    host = HOST
    tasks = [DefLogin]
    wait_time = between(3,5)

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)

class HelpVoiceAssistant(HttpUser):
    host = HOST
    tasks = [DefHelpVoiceAssistant]
    wait_time= between(3,5)   

class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)

class Logout(HttpUser):
    host = HOST
    tasks = [DefLogOut]
    wait_time= between(3,5)


class Postproc(HttpUser):
    host = HOST
    tasks = [DefPostproc]
    wait_time = between(3,5)
    

class Register(HttpUser):
    USER_PREFIX = randint(0, 10000)

    wait_time= between(3,5)

    def on_start(self):
        self.user_to_register = {
            'username': '{}usuario{}'.format(Register.USER_PREFIX, randint(0, 10000)),
            'sex': 'M',
            'style': 'N',
            'password': 'password1234',
        }

    @task
    def register(self):
        self.usr= self.client.post("/authentication/register/", self.user_to_register)

    def on_quit(self):
        self.user_to_register = None

class ModifyUser(HttpUser):
    USER_MODIFIED = 'admin'
    PASS_MODIFIED = 'admin1234'

    with open('modifiableOptions.json') as f:
        MODIFIABLE_OPTIONS = json.loads(f.read())

    wait_time= between(3,5)

    @task
    def login(self):
        self.token = self.client.post("/authentication/login/", {
            "username": ModifyUser.USER_MODIFIED,
            "password": ModifyUser.PASS_MODIFIED,
        }).json()['token']

    @task
    def getuser(self):
        self.client.post("/authentication/getuser/", {'token': self.token })

    @task
    def changestyle(self):
        newStyle = choice(ModifyUser.MODIFIABLE_OPTIONS.get('styles'))
        self.client.post("/authentication/changestyle/", {'token': self.token, 'style': newStyle })

    @task
    def changesex(self):
        newSex = choice(ModifyUser.MODIFIABLE_OPTIONS.get('sex_types'))
        self.client.post("/authentication/changesex/", {'token': self.token, 'sex': newSex })

    @task
    def changeemail(self):
        newEmail = choice(ModifyUser.MODIFIABLE_OPTIONS.get('emails'))
        self.client.post("/authentication/changeemail/", {'token': self.token, 'email': newEmail })

    @task
    def changeusername(self):
        newUsername = 'usuario{}'.format(randint(0, 10000))
        response = self.client.post("/authentication/modify/", {'token': self.token, 'username': newUsername })
        if response.status_code == 200:
            ModifyUser.USER_MODIFIED = newUsername
            print('New username is %s', ModifyUser.USER_MODIFIED)

    def on_quit(self):
        self.token = None