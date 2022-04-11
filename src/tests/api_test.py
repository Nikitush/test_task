import pytest

from config_test import DATA_FOR_CREATE_CONTACT_TESTS, DATA_FOR_GET_ALL_CONTACTS_TESTS_WITHOUT_DATA,\
    DATA_FOR_GET_ALL_CONTACTS_TESTS, DATA_FOR_GET_CONTACT_BY_ID_TESTS, DATA_FOR_DELETE_CONTACT_BY_ID_TESTS,\
    DATA_FOR_UPDATE_CONTACT_BY_ID_TESTS, DATA_FOR_CONTACT_INFO_AFTER_UPDATE_TESTS, PREPARED_CONTACTS


@pytest.mark.usefixtures('init_test_class')
class TestAPI:

    @pytest.mark.create_contact
    @pytest.mark.parametrize('data', DATA_FOR_CREATE_CONTACT_TESTS)
    def test_add_contact_endpoint(self, data, delete_all_contacts_after_tests):
        response = self.api.create_contact(json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])
        if data["status_code"] == 200:
            data["data"]["id"] = data["body"]["id"]
            for key in PREPARED_CONTACTS[0].keys():
                if key not in data["data"].keys():
                    data["data"][key] = None
            response = self.api.get_contact_by_id(contact_id=data["body"]["id"])
            assert response.status_code_should_be(data["status_code"])
            assert response.body_should_be(data["data"])

    @pytest.mark.get_all_contacts
    @pytest.mark.parametrize('data', DATA_FOR_GET_ALL_CONTACTS_TESTS_WITHOUT_DATA)
    def test_get_all_contacts_endpoint_without_data(self, data, delete_all_contacts_after_tests):
        response = self.api.get_all_contacts(json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])

    @pytest.mark.get_all_contacts
    @pytest.mark.parametrize('data', DATA_FOR_GET_ALL_CONTACTS_TESTS)
    def test_get_all_contacts_endpoint(self, data, create_prepared_contacts, delete_all_contacts_after_tests):
        response = self.api.get_all_contacts(json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])

    @pytest.mark.get_contact_by_id
    @pytest.mark.parametrize('data', DATA_FOR_GET_CONTACT_BY_ID_TESTS)
    def test_get_contact_by_id_endpoint(self, data, create_prepared_contacts, delete_all_contacts_after_tests):
        response = self.api.get_contact_by_id(contact_id=data["contact_id"], json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])

    @pytest.mark.delete_contact_by_id
    @pytest.mark.parametrize('data', DATA_FOR_DELETE_CONTACT_BY_ID_TESTS)
    def test_delete_contact_by_id_endpoint(self, data, create_prepared_contacts, delete_all_contacts_after_tests):
        response = self.api.delete_contact_by_id(contact_id=data["contact_id"], json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])
        if data["status_code"] == 200:
            response = self.api.get_contact_by_id(contact_id=data["contact_id"])
            assert response.status_code_should_be(data["get_status"])

    @pytest.mark.update_contact_by_id
    @pytest.mark.parametrize('data', DATA_FOR_UPDATE_CONTACT_BY_ID_TESTS)
    def test_update_contact_by_id_endpoint(self, data, create_prepared_contacts, delete_all_contacts_after_tests):
        response = self.api.update_contact_by_id(contact_id=data["contact_id"], json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])

    @pytest.mark.contact_info_after_update
    @pytest.mark.parametrize('data', DATA_FOR_CONTACT_INFO_AFTER_UPDATE_TESTS)
    def test_contact_info_after_update(self, data, create_prepared_contacts, delete_all_contacts_after_tests):
        if data["data"]:
            response = self.api.update_contact_by_id(contact_id=data["contact_id"], json=data["data"])
        else:
            response = self.api.get_contact_by_id(contact_id=data["contact_id"], json=data["data"])
        assert response.status_code_should_be(data["status_code"])
        assert response.body_should_be(data["body"])
