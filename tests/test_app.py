from http import HTTPStatus


def test_read_rood_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # assert
