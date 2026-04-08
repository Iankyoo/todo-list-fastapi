from http import HTTPStatus

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_create_user_via_api(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@exemple.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@exemple.com',
        'username': 'alice',
    }


def test_create_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Ian',
            'email': 'kyo@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Kyo',
            'email': 'contato.iankyoo@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_with_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_should_return_forbidden(client, token):
    response = client.put(
        '/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'newpassword',
            'id': 1,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@fausto.com',
            'password': 'secret',
        },
    )

    response = client.put(
        '/users/1',
        json={
            'username': 'fausto',
            'email': 'new@exemple.com',
            'password': 'secret',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User has been deleted'}


def test_create_usermodel():
    user = User(username='Ian', email='ian@exemple.com', password='secret')

    assert user.password == 'secret'


def test_read_user_with_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_with_id_should_return_404_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
