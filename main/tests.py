from unittest.mock import ANY
import pytest
from user.tests import reg_login


@pytest.mark.django_db
def test_iter(client, reg_login):
    response = client.get('/iter/', HTTP_Authorization="Token " + reg_login[3].data)
    assert response.status_code == 200
    assert response.json() == {'username': 'test', 'id': ANY}


@pytest.mark.django_db
def test_user_matched_reaction(client, reg_login):
    response1 = client.post(f'/reaction/{reg_login[0]}/', HTTP_Authorization='Token ' + reg_login[3].data)
    response2 = client.post(f'/reaction/{reg_login[1]}/', HTTP_Authorization='Token ' + reg_login[2].data)
    assert response1.status_code == 200
    assert response2.status_code == 200
    response3 = client.get('/user-matched/', HTTP_Authorization='Token ' + reg_login[2].data)
    assert response3.status_code == 200
    assert response3.json() == [{'username': 'test3', 'email': 'test3@gmail.com'}]


@pytest.mark.django_db
def test_message(client, reg_login):
    response = client.post(
        f'/message/{reg_login[0]}/', HTTP_Authorization='Token ' + reg_login[3].data, data={'message': "123"}
    )
    assert response.status_code == 200
    response1 = client.get(f'/message/{reg_login[0]}/', HTTP_Authorization='Token ' + reg_login[3].data)
    assert response1.json() == {'all_messages': [{'who': ANY, 'whom': ANY, 'message': '123'}]}
