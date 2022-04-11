FROM ubuntu:20.04
LABEL maintainer="071299nik@mail.ru"
WORKDIR /opt/test-server
COPY ["./test-server/main.py", "./test-server/__init__.py", "./test-server/database.py", "./test-server/requirements.txt", "./"]
COPY ./test-server/config config/
COPY ./test-server/service_config/test-server.service /etc/systemd/system
RUN apt-get update && apt-get -y upgrade && apt-get -y install systemctl python3 python3-pip python3-venv sqlite3 \
    build-essential libssl-dev libffi-dev python3-dev && \
    python3 -m venv venv && ./venv/bin/pip3 install -r requirements.txt
WORKDIR /opt/test-framework
COPY ["./test-framework/setup.py", "./test-framework/MANIFEST.in", "./test-framework/requirements.txt", "./"]
COPY ./test-framework/framework framework/
RUN python3 -m venv venv && ./venv/bin/pip3 install -r requirements.txt && \
    ./venv/bin/python3 setup.py sdist && ./venv/bin/pip3 install ./dist/* && \
    ls --hide=venv | xargs -d '\n' rm -r
WORKDIR /opt/tests
COPY ["./tests/api_test.py", "./tests/conftest.py", "./tests/config_test.py", "./tests/pytest.ini", "./"]