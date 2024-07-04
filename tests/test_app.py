from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_rood_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'testtest',
            'email': 'teste@gmail.com',
        },
    )
    # Valida o status de retorno
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'teste@gmail.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(
        user
    ).model_dump()  # comverte o usuario do pydetic no user public
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '1234',
            'username': 'testusername2',
            'email': 'teste@gmail.com',
            'id': user.id,
        },
    )
    #    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'email': 'teste@gmail.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    #    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
