import pytest
from faker import Faker

from db import (
    create_customer,
    get_customer_by_id,
    update_customer,
    get_max_customer_id,
    delete_customer,
    get_count_customers,
)


@pytest.fixture()
def customer_data() -> dict:
    fake = Faker("ru_RU")
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "email": fake.email(),
        "telephone": fake.phone_number(),
        "password": fake.password(),
    }


@pytest.fixture()
def updated_data() -> dict:
    return {
        "firstname": "test_firstname",
        "lastname": "test_lastname",
        "email": "email@example.com",
        "telephone": "123456789",
    }


@pytest.fixture()
def created_customer(connection, customer_data):
    customer_id = create_customer(connection, customer_data)
    yield customer_id
    delete_customer(connection, customer_id)


@pytest.fixture()
def non_existed_customer_id(connection) -> int:
    max_customer_id = get_max_customer_id(connection)
    return max_customer_id + 1 if max_customer_id else 1


@pytest.fixture()
def customers_count(connection) -> int:
    return get_count_customers(connection)


def test_create_customer(connection, customer_data):
    customer_id = create_customer(connection, customer_data)
    customer = get_customer_by_id(connection, customer_id)
    for field_to_check in customer:
        assert customer[field_to_check] == customer_data[field_to_check]
    delete_customer(connection, customer_id)


def test_update_customer(connection, updated_data, created_customer):
    update_customer(connection, created_customer, updated_data)
    customer = get_customer_by_id(connection, created_customer)
    assert customer == updated_data


def test_update_customer_negative(connection, non_existed_customer_id, updated_data):
    update_customer(connection, non_existed_customer_id, updated_data)
    customer = get_customer_by_id(connection, non_existed_customer_id)
    assert customer is None


def test_delete_customer(connection, created_customer):
    delete_customer(connection, created_customer)
    customer = get_customer_by_id(connection, created_customer)
    assert customer is None


def test_delete_customer_negative(connection, non_existed_customer_id, customers_count):
    delete_customer(connection, non_existed_customer_id)
    assert get_count_customers(connection) == customers_count
