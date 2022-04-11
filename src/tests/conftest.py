import pytest

from framework.api import API
from config_test import PREPARED_CONTACTS


def pytest_addoption(parser):
    parser.addoption('--host', action='store')
    parser.addoption('--port', action='store', default=None)


@pytest.fixture(scope="class")
def init_test_class(request):
    host = request.config.getoption("host")
    port = request.config.getoption("port")
    request.cls.api = API(host=host, port=port)


@pytest.fixture(scope="function")
def delete_all_contacts_after_tests(request):
    yield
    response = request.cls.api.get_all_contacts()
    for record in response.body:
        request.cls.api.delete_contact_by_id(contact_id=record["id"])


@pytest.fixture(scope="function")
def create_prepared_contacts(request):
    for record in PREPARED_CONTACTS:
        request.cls.api.create_contact(json=record)
    yield
