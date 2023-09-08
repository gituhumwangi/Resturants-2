#!/usr/bin/env python3

from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Restaurant, Review, Customer, restaurants_customer

if __name__ == '__main__':

    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb; ipdb.set_trace()
