from sqlalchemy import (create_engine, Table, Column, ForeignKey, Integer, String, MetaData)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///resturants.db')
Session = sessionmaker(bind=engine)
session = Session()

restaurant_customer = Table(
    'restaurant_users',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key =True),
    Column('customer_id', ForeignKey('customers.id'), primary_key = True  ),
    extend_existing = True,

)

class Restaurants(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer(), primary_key = True)
    name = Column(String())
    price = Column(Integer())
    review = relationship('Review', backref=backref('restaurant'))
    customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')

    def __repr__(self):
        return f'Resturants(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'
    
    def fanciest(cls):
        # Return the restaurant instance with the highest price
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        # Return a list of strings with all the reviews for this restaurant
        review_strings = []
        for review in self.reviews:
            review_strings.append(f"Review for {self.name} by {review.customer.full_name()}: {review.rating} stars.")
        return review_strings


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key = True)
    first_name = Column(String())
    last_name = Column(String())
    review=relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurants', secondary=restaurant_customer, back_populates='customers')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        # Query and return the restaurant with the highest star rating from this customer's reviews
        highest_rating = 0
        favorite_restaurant = None
        for review in self.reviews:
            if review.rating > highest_rating:
                highest_rating = review.rating
                favorite_restaurant = review.restaurant
        return favorite_restaurant
    def add_review(self, restaurant, rating):
        # Create a new review for the restaurant with the given rating
        review = Review(customer=self, restaurant=restaurant, rating=rating)
        session.add(review)
        session.commit()

    def delete_reviews(self, restaurant):
        # Delete all reviews by this customer for the specified restaurant
        session.query(Review).filter(Review.customer == self, Review.restaurant == restaurant).delete()
        session.commit()

    def reviews(self):
        return self.reviews

    def restaurants(self):
        # Return a collection of all the restaurants that the customer has reviewed
        return [review.restaurant for review in self.reviews]


    def __repr__(self):
        return f'Customer(id={self.id}, ' + \
           f'first_name={self.first_name}, ' + \
           f'last_name={self.last_name})'
    
   


class Review(Base):
    pass
    __tablename__ = 'reviews'
    id = Column(Integer(), primary_key = True)
    comments = Column(String())
    rating = Column(Integer())
    customer_id=Column(Integer(), ForeignKey('customers.id'))
    restaurants_id=Column(Integer(), ForeignKey('restaurants.id'))

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'comments={self.comments},)'
    
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.rating} stars."

