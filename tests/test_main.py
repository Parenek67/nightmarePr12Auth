import requests

api_url = 'http://localhost:8000'

def test_healthcheck():
    responce = requests.get(f'{api_url}/__health')
    assert responce.status_code == 200

class TestAuth():
    def test_get_users(self):
        responce = requests.get(f'{api_url}/v1/users')
        assert responce.status_code == 200
        assert len(responce.json()) == 50

    def test_add_user(self):
        body = { "name": "Vasya", "login": "vasyan123", "password": "pass123" }
        responce = requests.post(f'{api_url}/v1/postusers', json = body)
        assert responce.status_code == 200  

    def auth_user(self):
        responce = requests.get(f'{api_url}/v1/users/vasyan123/pass123')
        assert responce.status_code == 200

    def test_users_count(self):
        responce = requests.get(f'{api_url}/v1/users')
        assert responce.status_code == 200
        assert len(responce.json()) == 1    

