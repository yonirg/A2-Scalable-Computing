from dataclasses import dataclass
from faker import Faker
from functools import wraps
from dataclasses import dataclass
import time
import datetime

@dataclass
class User:
    id: str
    name: str
    email: str
    address: str
    registration_date: str
    birth_date: str

@dataclass
class Product:
    id: str
    name: str
    image: str
    description: str
    price: float

@dataclass
class Store:
    id: str
    name: str
    url: str

@dataclass
class Stock:
    id_product: str
    id_store: str
    quantity: int

@dataclass
class Purchase_Order:
    user_id: str
    product_id: str
    store_id: str
    quantity: int
    creation_date: str
    payment_date: str
    delivery_date: str

@dataclass
class Purchase_History:
    user_id: str
    total_value: float
    timestamp: datetime.datetime

# Singleton decorator
def singleton(cls):
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    return wrapper

@singleton
class FakerSingleton:
    def __init__(self):
        self._faker = None

    def get_faker(self):
        if not self._faker:
            self._faker = Faker()
        return self._faker


def generate_user():
    """Generates a User dataclass instance with unique data."""
    faker = FakerSingleton().get_faker()
    return User(
        id=faker.unique.numerify(text="1########"),
        name=faker.name(),
        email=faker.email(),
        address= f"{faker.street_address()}, {faker.city()}, {faker.state()}, {faker.zipcode()}, {faker.country()}",
        registration_date = str(time.time_ns()),
        birth_date=faker.date_of_birth(minimum_age=18, maximum_age=100).isoformat(),
    )

def generate_product():
    """Generates a Product dataclass instance with unique data."""
    faker = FakerSingleton().get_faker()

    return Product(
        id=faker.unique.numerify(text="2######"),
        name=faker.word(),
        image=faker.image_url(),
        description=faker.sentence(),
        price=faker.random_int(min=1, max=1000),
    )

def generate_store():
    """Generates a Store dataclass instance with unique data."""
    faker = FakerSingleton().get_faker()
    return Store(
        id=faker.unique.numerify(text="3######"),
        name=faker.company(),
        url=faker.url(),
    )


def generate_stock(product_id: str, store_id: str, quantity: int):
    """Generates a Stock dataclass instance with unique data."""
    faker = FakerSingleton().get_faker()
    return Stock(
        id_product=product_id,
        id_store=store_id,
        quantity=quantity,
    )

def generate_purchase_order(user_id: str, product_id: str, store_id: str, quantity: int) -> Purchase_Order:
    faker = FakerSingleton().get_faker()
    
    # Generate random dates within a year
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    
    creation_date = faker.date_time_between(start_date=start_date, end_date=end_date)
    payment_date = faker.date_time_between(start_date=creation_date, end_date=end_date)
    delivery_date = faker.date_time_between(start_date=payment_date, end_date=end_date)
    
    return Purchase_Order(
        user_id=user_id,
        product_id=product_id,
        store_id=store_id,
        quantity=quantity,
        creation_date=creation_date.isoformat(),
        payment_date=payment_date.isoformat(),
        delivery_date=delivery_date.isoformat()
    )


def generate_purchase_order_recent(user_id: str, product_id: str, store_id: str, quantity: int) -> Purchase_Order:
    faker = FakerSingleton().get_faker()
    
    # Generate random dates within a year
    start_date = datetime.now() - timedelta(minutes=5)
    end_date = datetime.now()
    
    creation_date = faker.date_time_between(start_date=start_date, end_date=end_date)
    payment_date = faker.date_time_between(start_date=creation_date, end_date=end_date)
    delivery_date = faker.date_time_between(start_date=payment_date, end_date=end_date)
    
    return Purchase_Order(
        user_id=user_id,
        product_id=product_id,
        store_id=store_id,
        quantity=quantity,
        creation_date=creation_date.isoformat(),
        payment_date=payment_date.isoformat(),
        delivery_date=delivery_date.isoformat()
    )
