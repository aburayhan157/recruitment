from . import api_service


def login(data):
    headers = {
        'Content-Type': 'application/json'
    }

    return api_service.post('login/', headers, data)


def apply(auth_token, data):
    headers = {
        'Authorization': 'token {}'.format(auth_token),
        'Content-Type': 'application/json'
    }

    return api_service.post('v1/recruiting-entities/', headers, data)


def upload(auth_token, file_token_id, files):
    headers = {
        'Authorization': 'token {}'.format(auth_token),
    }

    return api_service.put('file-object/' + str(file_token_id) + '/', headers, files)
