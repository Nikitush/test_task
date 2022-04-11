from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


Base = declarative_base()


class Contact(Base):
    __tablename__ = "Contact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text)
    phone = Column(Text)
    country = Column(Text)
    city = Column(Text)
    address = Column(Text)


def key_exist_in_json(key, js):
    if key in js.keys():
        return js[key]
    else:
        return None


def setup_engine(db_path):
    return create_engine(db_path)


def create_db(engine):
    Base.metadata.create_all(engine)


def add_contact_to_db(engine, data):
    record = Contact(email=key_exist_in_json(key="email", js=data),
                     first_name=key_exist_in_json(key="first_name", js=data),
                     last_name=key_exist_in_json(key="last_name", js=data),
                     phone=key_exist_in_json(key="phone", js=data),
                     country=key_exist_in_json(key="country", js=data),
                     city=key_exist_in_json(key="city", js=data),
                     address=key_exist_in_json(key="address", js=data))
    session = sessionmaker(bind=engine)()
    session.add(record)
    session.commit()
    contact_id = record.id
    session.close()
    return contact_id


def get_all_contacts_from_db(engine):
    session = sessionmaker(bind=engine)()
    records = session.query(Contact).all()
    session.close()
    return records


def get_contact_from_db(engine, contact_id):
    session = sessionmaker(bind=engine)()
    record = session.query(Contact).filter(Contact.id == contact_id).one()
    session.close()
    return record


def delete_contact_from_db(engine, contact_id):
    session = sessionmaker(bind=engine)()
    record = session.query(Contact).filter(Contact.id == contact_id).one()
    session.delete(record)
    session.commit()
    session.close()


def update_contact_from_db(engine, contact_id, data):
    session = sessionmaker(bind=engine)()
    session.query(Contact).filter(Contact.id == contact_id).update(data)
    session.commit()
    session.close()
