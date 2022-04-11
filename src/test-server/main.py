from flask import Flask, jsonify, request
import argparse
import yaml
import signal
import sys
from os.path import exists, abspath, join
from os import makedirs
import logging

from database import create_db, setup_engine, add_contact_to_db, get_all_contacts_from_db, get_contact_from_db, \
    delete_contact_from_db, update_contact_from_db, key_exist_in_json, NoResultFound


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


logging.basicConfig(
     filename='/var/log/test-server.log',
     level=logging.DEBUG,
     format='[%(asctime)s]  [%(levelname)s] - %(message)s'
)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


fields = ("id", "email", "first_name", "last_name", "phone", "country", "city", "address")


@app.errorhandler(404)
def internal_server_error(error):
    app.logger.error(f"Method {request.method} {request.path} not found.")
    return jsonify({"message": f"method {request.method} {request.path} not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.error(f"Method {request.method} {request.path} not allowed.")
    return jsonify({"message": f"method {request.method} {request.path} not allowed"}), 405


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f"Internal Server error: {error}")
    return jsonify({"message": f"{error}"}), 500


@app.route("/api/contacts", methods=["GET"])
def get_all_contacts():
    if request.data:
        app.logger.error("Endpoint GET /api/contacts. Status code: 400. This endpoint don't support some data in request.")
        return jsonify({"message": "contacts method GET don't should be contain some data, maybe you want use POST method?"}), 400
    response = list()
    for record in get_all_contacts_from_db(engine=engine):
        response.append({"id": record.id, "email": record.email, "first_name": record.first_name,
                         "last_name": record.last_name, "phone": record.phone, "country": record.country,
                         "city": record.city, "address": record.address})
    app.logger.info("Endpoint GET /api/contacts. Status code: 200.")
    return jsonify(response), 200


@app.route("/api/contacts", methods=["POST"])
def add_contact():
    data = request.json
    exclude_fields = list()
    for key in data.keys():
        if key not in fields:
            exclude_fields.append(key)
    if exclude_fields:
        app.logger.error(f"Endpoint POST /api/contacts. Status code 400. This endpoint don't should be contain fields from list:{exclude_fields}")
        return jsonify({"message": f"contact don't should be contain fields from list:{exclude_fields}"}), 400
    elif "first_name" not in data.keys() and "email" not in data.keys():
        app.logger.error("Endpoint POST /api/contacts. Status code 400. This endpoint should be contain first_name and email fields")
        return jsonify({"message": "contact should be contain first_name and email fields"}), 400
    elif "first_name" not in data.keys():
        app.logger.error(f"Endpoint POST /api/contacts. Status code 400. This endpoint should be contain first_name field")
        return jsonify({"message": "contact should be contain first_name field"}), 400
    elif "email" not in data.keys():
        app.logger.error(f"Endpoint POST /api/contacts. Status code 400. This endpoint should be contain email field")
        return jsonify({"message": "contact should be contain email field"}), 400
    else:
        contact_id = add_contact_to_db(engine=engine, data=data)
        app.logger.info(f"Endpoint POST /api/contacts. Status code: 200. Contact data: id={key_exist_in_json(key='id',js=data)}, "
                        f"email={key_exist_in_json(key='email', js=data)}, first_name={key_exist_in_json(key='first_name', js=data)}, "
                        f"last_name={key_exist_in_json(key='last_name', js=data)}, phone={key_exist_in_json(key='phone', js=data)}, "
                        f"country={key_exist_in_json(key='country', js=data)}, city={key_exist_in_json(key='city', js=data)}, "
                        f"address={key_exist_in_json(key='address', js=data)}")
        return jsonify({"id": contact_id, "message": "contact added successfully"}), 200


@app.route("/api/contact/<contact_id>", methods=["GET"])
def get_contact_by_id(contact_id):
    try:
        record = get_contact_from_db(engine=engine, contact_id=contact_id)
        if request.data:
            app.logger.error("Endpoint GET /api/contact/<contact_id>. Status code: 400. This endpoint don't support some data in request.")
            return jsonify({"message": "contact method GET don't should be contain some data, maybe you want use PUT method?"}), 400
        response = dict({"id": record.id, "email": record.email, "first_name": record.first_name,
                         "last_name": record.last_name, "phone": record.phone, "country": record.country,
                         "city": record.city, "address": record.address})
        app.logger.info(f"Endpoint GET /api/contact/<contact_id>. Status code: 200. Contact data: id={record.id}, " 
                        f"email={record.email}, first_name={record.first_name}, last_name={record.last_name}, "
                        f"phone={record.phone}, country={record.country}, city={record.city}, address={record.address}")
        return jsonify(response), 200
    except NoResultFound:
        app.logger.error(f"Endpoint GET /api/contact/<contact_id>. Status code: 404. Contact with id: {contact_id} don't exist")
        return jsonify({"message": f"contact with id: {contact_id} don't exist"}), 404


@app.route("/api/contact/<contact_id>", methods=["DELETE"])
def delete_contact_by_id(contact_id):
    try:
        get_contact_from_db(engine=engine, contact_id=contact_id)
        if request.data:
            app.logger.error("Endpoint DELETE /api/contact/<contact_id>. Status code: 400. This endpoint don't support some data in request.")
            return jsonify({"message": "contact method DELETE don't should be contain some data, maybe you want use PUT method?"}), 400
        delete_contact_from_db(engine=engine, contact_id=contact_id)
        app.logger.info(f"Endpoint DELETE /api/contact/<contact_id>. Status code: 200. Contact with id: {contact_id} delete successfully")
        return jsonify({"message": f"contact delete successfully"}), 200
    except NoResultFound:
        app.logger.error(f"Endpoint DELETE /api/contact/<contact_id>. Status code: 404. Contact with id: {contact_id} don't exist")
        return jsonify({"message": f"contact with id: {contact_id} don't exist"}), 404


@app.route("/api/contact/<contact_id>", methods=["PUT"])
def update_contact_info_by_id(contact_id):
    try:
        get_contact_from_db(engine=engine, contact_id=contact_id)
        data = request.json
        exclude_fields = list()
        for key in data.keys():
            if key not in fields:
                exclude_fields.append(key)
        if exclude_fields:
            app.logger.error(f"Endpoint PUT /api/contact/<contact_id>. Status code: 400. This endpoint don't should be contain fields from list:{exclude_fields}")
            return jsonify({"message": f"contact don't should be contain fields from list:{exclude_fields}"}), 400
        else:
            update_contact_from_db(engine=engine, contact_id=contact_id, data=data)
            app.logger.info(f"Endpoint PUT /api/contact/<contact_id>. Status code: 200. Contact with id: {contact_id} "
                            f"apdate fields: {data}")
            return jsonify({"message": "contact update successfully"}), 200
    except NoResultFound:
        app.logger.error(f"Endpoint PUT /api/contact/<contact_id>. Status code: 404. Contact with id: {contact_id} don't exist")
        return jsonify({"message": f"contact with id: {contact_id} don't exist"}), 404


def signal_term_handler(signal, frame):
    engine.dispose()
    app.logger.info("App Server finished.")
    sys.exit(0)


if __name__ == "__main__":
    try:
        app.logger.info("App Server starting...")
        signal.signal(signal.SIGTERM, signal_term_handler)
        parser = argparse.ArgumentParser(description="Server configuration options")
        parser.add_argument("--config_path", help="Input port")
        args = parser.parse_args()
        with open(args.config_path, 'r') as config_file:
            config = yaml.load(stream=config_file, Loader=yaml.FullLoader)
        if exists(path=abspath(join(config["root_path"], "database/server.db"))) is True:
            engine = setup_engine(db_path=f'sqlite:///{config["db_path"]}')
        else:
            app.logger.info("Database create starting...")
            makedirs(name=join(config["root_path"], "database"))
            engine = setup_engine(db_path=f'sqlite:///{config["db_path"]}')
            create_db(engine=engine)
            app.logger.info("Database successfully created.")
        app.run(app.logger.info("App Server successfully started."), port=config["port"])
    except Exception as e:
        app.logger.error(f"Server don't start with error: {e}")
