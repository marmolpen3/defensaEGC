import json
import requests


HOST = "http://localhost:8000"
USER = "decidedb"
PASS = "complexpassword"
VOTING = 1


def create_voters(filename):

    with open(filename) as f:
        voters = json.loads(f.read())

    data = {'username': USER, 'password': PASS, 'sex': 'M', 'style': 'N'}
    response = requests.post(HOST + '/authentication/login/', data=data)
    token = response.json()

    votersUser = []
    invalid_voters = []
    for username, pwd in voters.items():
        token.update({'username': username, 'password': pwd, 'sex': 'M', 'style': 'N'})
        response = requests.post(HOST + '/authentication/register/', data=token)
        if response.status_code == 201:
            votersUser.append(response.json().get('user_pk'))
        else:
            invalid_voters.append(username)
    return votersUser, invalid_voters

def add_census(voters_pk, voting_pk):
    """
    Add to census all voters_pk in the voting_pk.
    """
    data = {'username': USER, 'password': PASS}
    response = requests.post(HOST + '/authentication/login/', data=data)
    token = response.json()

    data2 = {'voters': voters_pk, 'voting_id': voting_pk}
    auth = {'Authorization': 'Token ' + token.get('token')}
    response = requests.post(HOST + '/census/', json=data2, headers=auth)

voters, invalids = create_voters('voters.json')
add_census(voters,VOTING)
print("Create voters with pk={0} \nInvalid usernames={1}".format(voters, invalids))
