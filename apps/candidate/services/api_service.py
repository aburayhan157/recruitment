import requests


ROOT_URL = 'https://recruitment.fisdev.com/api/'


def post(uri, headers, data):
    return requests.post(ROOT_URL + uri, headers=headers, data=data)


def put(uri, headers, files):
    return requests.put(ROOT_URL + uri, headers=headers, files=files)
