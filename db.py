from datetime import date

import pymysql


def create_customer(connection, customer_data: dict) -> int:
    with connection.cursor() as cursor:
        sql = "INSERT INTO oc_customer (customer_group_id, language_id, firstname, lastname, email, telephone, password, custom_field, ip, status, safe, token,code, date_added) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            sql,
            (
                1,
                0,
                customer_data["firstname"],
                customer_data["lastname"],
                customer_data["email"],
                customer_data["telephone"],
                customer_data["password"],
                "",
                "",
                1,
                0,
                "",
                "",
                date.today(),
            ),
        )
    connection.commit()
    return cursor.lastrowid


def update_customer(connection, customer_id: int, update_data) -> None:
    with connection.cursor() as cursor:
        sql = "UPDATE oc_customer SET firstname = %s, lastname = %s, email = %s, telephone = %s WHERE customer_id = %s"
        cursor.execute(
            sql,
            (
                update_data["firstname"],
                update_data["lastname"],
                update_data["email"],
                update_data["telephone"],
                customer_id,
            ),
        )
    connection.commit()


def delete_customer(connection, customer_id: int) -> None:
    with connection.cursor() as cursor:
        sql = "DELETE FROM oc_customer WHERE customer_id = %s"
        cursor.execute(sql, (customer_id,))
    connection.commit()


def get_customer_by_id(connection, customer_id: int) -> dict:
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT firstname, lastname, email, telephone FROM oc_customer WHERE customer_id = %s"
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


def get_max_customer_id(connection) -> int:
    with connection.cursor() as cursor:
        sql = "SELECT max(customer_id) FROM oc_customer"
        cursor.execute(sql)
        return cursor.fetchone()[0]


def get_count_customers(connection) -> int:
    with connection.cursor() as cursor:
        sql = "SELECT count(customer_id) FROM oc_customer"
        cursor.execute(sql)
        return cursor.fetchone()[0]
