import pytest
import pymysql


def pytest_addoption(parser):
    parser.addoption(
        "--host", action="store", default="192.168.0.108", help="Database host"
    )
    parser.addoption("--port", action="store", default=3306, help="Database port")
    parser.addoption(
        "--database", action="store", default="bitnami_opencart", help="Database name"
    )
    parser.addoption(
        "--user", action="store", default="bn_opencart", help="Database user"
    )
    parser.addoption("--password", action="store", default="", help="Database password")


@pytest.fixture(scope="session")
def connection(request):
    host = request.config.getoption("--host")
    port = request.config.getoption("--port")
    database = request.config.getoption("--database")
    user = request.config.getoption("--user")
    password = request.config.getoption("--password")

    connect = pymysql.connect(
        host=host, port=int(port), user=user, password=password, database=database
    )
    yield connect
    connect.close()
