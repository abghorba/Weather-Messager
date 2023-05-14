import pytest

from src.utilities import PostgresCredentials


@pytest.mark.skipif(PostgresCredentials().empty_credentials, reason="PostgreSQL Database credentials not provided!")
class TestPostgresDatabaseHandler:
    def test_connect_to_database(self):
        pass

    def test_close_database_connection(self):
        pass

    def test_execute_simple_sql(self):
        pass

    def test_execute_sql_parametrized(self):
        pass

    def test_execute_sql(self):
        pass
