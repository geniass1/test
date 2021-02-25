import pytest


@pytest.mark.django_db
@pytest.fixture
def reg_login(client):
    response1 = client.post('/user/reg/', data={'username': 'test', 'email': 'test@gmail.com', 'password': 'test'})
    response2 = client.post('/user/reg/', data={'username': 'test3', 'email': 'test3@gmail.com', 'password': 'test'})
    response3 = client.post('/user/login/', data={'username': 'test', 'password': 'test'})
    response4 = client.post('/user/login/', data={'username': 'test3', 'password': 'test'})
    return response1.data['id'], response2.data['id'], response3, response4


@pytest.mark.django_db
def test_register(client):
    response = client.post(
        '/user/reg/', data={'username': 'test', 'email': 'test@gmail.com', 'password': 'test'}, format='json'
    )
    client.post(
        '/user/reg/', data={'username': 'test3', 'email': 'test3@gmail.com', 'password': 'test3'}, format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(client, reg_login):
    response = client.post(
        '/user/login/', data={'username': 'test', 'password': 'test'}, format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_change(client, reg_login):
    response = client.post(
        '/user/change/',
        data={
            'username': 'test',
            'password': 'test',
            'new_username': 'test2',
            'new_password': 'test2',
            'subscription': 'VIP'
        },
        format='json'
    )
    assert response.status_code == 200
