DATA_FOR_CREATE_CONTACT_TESTS = [{"status_code": 400,
                                  "data": {"name": "Nik", "age": "22"},
                                  "body": {"message": "contact don't should be contain fields from list:['name', 'age']"}},
                                 {"status_code": 400,
                                  "data": {"city": "Moscow", "country": "Russia"},
                                  "body": {"message": "contact should be contain first_name and email fields"}},
                                 {"status_code": 400,
                                  "data": {"email": "071299nik@mail.ru", "city": "Moscow"},
                                  "body": {"message": "contact should be contain first_name field"}},
                                 {"status_code": 400,
                                  "data": {"first_name": "Nik", "city": "Moscow"},
                                  "body": {"message": "contact should be contain email field"}},
                                 {"status_code": 200,
                                  "data": {"first_name": "Nik", "email": "Moscow"},
                                  "body": {"id": 1, "message": "contact added successfully"}}
                                 ]

PREPARED_CONTACTS = [{"email": "071299nik@mail.ru", "first_name": "Nik",
                      "last_name": "Isaak", "phone": "89156871357", "country": "Russia",
                      "city": "Zelenograd", "address": "k.601"},
                     {"email": "071200nik@mail.ru", "first_name": "Nik",
                      "last_name": "Isaak", "phone": "89156871723", "country": "Russia",
                      "city": "Zelenograd", "address": "k.601"},
                     ]


def update_prepared_contacts(prepared_contacts, contact_id=None, params=None):
    prepared_contacts_new = list()
    for i, contact in enumerate(prepared_contacts):
        i += 1
        contact["id"] = i
        prepared_contacts_new.append(contact)
    if contact_id and params:
        for key, value in params.items():
            prepared_contacts_new[contact_id][key] = value
        return prepared_contacts_new
    else:
        return prepared_contacts_new


DATA_FOR_GET_ALL_CONTACTS_TESTS_WITHOUT_DATA = [{"status_code": 400,
                                                 "data": {"some_key": "some_data"},
                                                 "body": {"message": "contacts method GET don't should be contain some data, maybe you want use POST method?"}},
                                                {"status_code": 200,
                                                 "data": None,
                                                 "body": list()}
                                                ]

DATA_FOR_GET_ALL_CONTACTS_TESTS = [{"status_code": 200,
                                    "data": None,
                                    "body": update_prepared_contacts(prepared_contacts=PREPARED_CONTACTS)}
                                   ]

DATA_FOR_GET_CONTACT_BY_ID_TESTS = [{"status_code": 400,
                                     "contact_id": 1,
                                     "data": {"some_key": "some_data"},
                                     "body": {"message": "contact method GET don't should be contain some data, maybe you want use PUT method?"}},
                                    {"status_code": 404,
                                     "contact_id": -100,
                                     "data": None,
                                     "body": {"message": "contact with id: -100 don't exist"}},
                                    {"status_code": 200,
                                     "contact_id": 1,
                                     "data": None,
                                     "body": update_prepared_contacts(prepared_contacts=PREPARED_CONTACTS)[0]}
                                    ]

DATA_FOR_DELETE_CONTACT_BY_ID_TESTS = [{"status_code": 400,
                                        "contact_id": 1,
                                        "data": {"some_key": "some_data"},
                                        "body": {"message": "contact method DELETE don't should be contain some data, maybe you want use PUT method?"}},
                                       {"status_code": 404,
                                        "contact_id": -100,
                                        "data": None,
                                        "body": {"message": "contact with id: -100 don't exist"}},
                                       {"status_code": 200,
                                        "contact_id": 1,
                                        "data": None,
                                        "body": {"message": "contact delete successfully"},
                                        "get_status": 404}
                                       ]

DATA_FOR_UPDATE_CONTACT_BY_ID_TESTS = [{"status_code": 400,
                                        "contact_id": 1,
                                        "data": {"some_key": "some_data", "second_some_key": "second_some_data"},
                                        "body": {"message": "contact don't should be contain fields from list:['some_key', 'second_some_key']"}},
                                       {"status_code": 404,
                                        "contact_id": -100,
                                        "data": None,
                                        "body": {"message": "contact with id: -100 don't exist"}},
                                       {"status_code": 200,
                                        "contact_id": 1,
                                        "data": {"first_name": "Nikita"},
                                        "body": {"message": "contact update successfully"}}
                                       ]

DATA_FOR_CONTACT_INFO_AFTER_UPDATE_TESTS = [{"status_code": 200,
                                             "contact_id": 1,
                                             "data": {"first_name": "Nikita"},
                                             "body": {"message": "contact update successfully"}},
                                            {"status_code": 200,
                                             "contact_id": 1,
                                             "data": None,
                                             "body": update_prepared_contacts(prepared_contacts=PREPARED_CONTACTS,
                                                                              contact_id=1,
                                                                              params={"first_name": "Nikita"})[0]}
                                            ]
