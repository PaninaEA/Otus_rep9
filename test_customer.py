from faker import Faker

from db import (
    create_customer,
    get_customer_by_id,
    update_customer,
    get_max_customer_id,
    delete_customer,
    get_count_customers,
)


def customer_data():
    fake = Faker("ru_RU")
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "email": fake.email(),
        "telephone": fake.phone_number(),
        "password": fake.password(),
    }


def updated_data():
    return {
        "firstname": "test_firstname",
        "lastname": "test_lastname",
        "email": "email@example.com",
        "telephone": "123456789",
    }


def test_create_customer(connection):
    customer_to_add = customer_data()
    customer_id = create_customer(connection, customer_to_add)
    customer = get_customer_by_id(connection, customer_id)
    assert customer["firstname"] == customer_to_add["firstname"]
    assert customer["lastname"] == customer_to_add["lastname"]
    assert customer["email"] == customer_to_add["email"]


def test_update_customer(connection):
    customer_to_update = customer_data()
    customer_id = create_customer(connection, customer_to_update)
    update_customer(connection, customer_id, updated_data())
    customer = get_customer_by_id(connection, customer_id)
    assert customer == updated_data()


def test_update_customer_negative(connection):
    max_customer_id = get_max_customer_id(connection)
    if max_customer_id > 0:
        customer_id = max_customer_id + 1
    else:
        customer_id = 1
    update_customer(connection, customer_id, updated_data())
    customer = get_customer_by_id(connection, customer_id)
    assert customer is None


def test_delete_customer(connection):
    customer_to_delete = customer_data()
    customer_id = create_customer(connection, customer_to_delete)
    delete_customer(connection, customer_id)
    customer = get_customer_by_id(connection, customer_id)
    assert customer is None


def test_delete_customer_negative(connection):
    count_customers = get_count_customers(connection)
    max_customer_id = get_max_customer_id(connection)
    if max_customer_id > 0:
        customer_id = max_customer_id + 1
    else:
        customer_id = 1
    delete_customer(connection, customer_id)
    assert get_count_customers(connection) == count_customers
