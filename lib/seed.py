from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

from model import Restaurants, Customer, Review  
from faker import Faker

if __name__ == '__main__':
    engine = create_engine('sqlite:///resturants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    fake = Faker()

    name = ['The Hungry Fork', 'Savory Bites', 'Spices Palace', 'Bella Italia', 'Sushi Sensation',
            'The Rustic Table', 'Chez Amis Brasserie', 'Thai Orchid Kitchen', 'The Grill House', 'Cafe Parisienne',
            'Tandoori Palace', 'Pizzaria Pizzazz', 'Seafood Shack', 'Veggie Delight Kitchen', 'Fusion Flavors',
            'La Fiesta Mexcian', 'Gourmet Garden', 'The Noddle House', 'Burger Bliss', 'Sweet Temptations Dessert Bar']

    restaurants = []
    for i in range(20):
        restaurant = Restaurants(
            name=random.choice(name),
            price=random.randint(1, 100),
        )

        session.add(restaurant)  
        session.commit()

        restaurants.append(restaurant)

    customers = []
    for i in range(100):
        customer = Customer(
            first_name=fake.unique.first_name(),  
            last_name=fake.unique.last_name(),
        )

        session.add(customer)  # Pass the customer object
        customers.append(customer)

    reviews = []
    for i in range(150):
        review = Review(
            comments=fake.sentence(),
            rating=random.randint(1, 10),
            restaurants_id=random.choice(restaurants).id,  # Randomly select a restaurant
            customer_id=random.choice(customers).id,  # Randomly select a customer
        )

        session.add(review)  

    session.commit()  
