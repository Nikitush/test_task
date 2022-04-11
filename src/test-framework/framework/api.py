from os.path import join
import requests

from .assertable_response import AssertableResponse
from .config import HEADERS


class API:

    def __init__(self, host, port=None):
        if not host.startswith('http://') and port is not None:
            self.__url = 'http://{}'.format(join(':'.join([host, port]), 'api'))
        elif not host.startswith('http://') and port is None:
            self.__url = 'http://{}'.format(join(host, 'api'))
        elif host.startswith('http://') and port is not None:
            self.__url = join(':'.join([host, port]), 'api')
        else:
            self.__url = join(host, 'api')

    def __get(self, *args, **kwargs):
        return AssertableResponse(requests.get(*args, **kwargs))

    def __post(self, *args, **kwargs):
        return AssertableResponse(requests.post(*args, **kwargs))

    def __put(self, *args, **kwargs):
        return AssertableResponse(requests.put(*args, **kwargs))

    def __delete(self, *args, **kwargs):
        return AssertableResponse(requests.delete(*args, **kwargs))

    def get_all_contacts(self, *args, **kwargs):
        request_url = join(self.__url, "contacts")
        return self.__get(url=request_url, headers=HEADERS, *args, **kwargs)

    def create_contact(self, *args, **kwargs):
        request_url = join(self.__url, "contacts")
        return self.__post(url=request_url, headers=HEADERS, *args, **kwargs)

    def get_contact_by_id(self, contact_id, *args, **kwargs):
        request_url = join(self.__url, join("contact", str(contact_id)))
        return self.__get(url=request_url, headers=HEADERS, *args, **kwargs)

    def delete_contact_by_id(self, contact_id, *args, **kwargs):
        request_url = join(self.__url, join("contact", str(contact_id)))
        return self.__delete(url=request_url, headers=HEADERS, *args, **kwargs)

    def update_contact_by_id(self, contact_id, *args, **kwargs):
        request_url = join(self.__url, join("contact", str(contact_id)))
        return self.__put(url=request_url, headers=HEADERS, *args, **kwargs)
