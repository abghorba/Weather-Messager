import pytest

from database.execute_sql import PostgresDatabaseHandler
from src.utilities import PostgresCredentials


@pytest.mark.skipif(PostgresCredentials().empty_credentials, reason="PostgreSQL Database credentials not provided!")
class TestPostgresDatabaseHandler:
    database_handler = PostgresDatabaseHandler()

    def test_close_database_connection(self):
        """Tests PostgresDatabaseHandler.close_database_connection()."""

        assert not self.database_handler.close_database_connection()

    def test_connect_to_database(self):
        """Tests PostgresDatabaseHandler.connect_to_database()."""

        assert not self.database_handler.connect_to_database()

    @pytest.mark.parametrize(
        "sql_queries,expected_value,expect_data",
        [
            ("SELECT * FROM test WHERE test_col1 = 'Testing1';", False, False),
            (
                [
                    "INSERT INTO test (test_col1, test_col2) VALUES ('Testing1', 'Testing2');",
                    "SELECT * FROM test WHERE test_col1 = 'Testing1';",
                ],
                False,
                True,
            ),
            (
                ["DELETE FROM test WHERE test_col1 = 'Testing1';", "SELECT * FROM test WHERE test_col1 = 'Testing1';"],
                False,
                False,
            ),
        ],
    )
    def test_execute_simple_sql(self, sql_queries, expected_value, expect_data):
        """Tests PostgresDatabaseHandler.execute_simple_sql()."""

        assert self.database_handler.execute_simple_sql(sql_queries=sql_queries) == expected_value
        data = self.database_handler.cursor.fetchone()

        if expect_data:
            assert data["test_col1"] == "Testing1"
            assert data["test_col2"] == "Testing2"

        else:
            assert data is None

    @pytest.mark.parametrize(
        "sql_queries,query_params,expected_value,expect_data",
        [
            ("SELECT * FROM test WHERE test_col1 = %s;", ("Testing1",), False, False),
            (
                [
                    "INSERT INTO test (test_col1, test_col2) VALUES (%s, %s);",
                    "SELECT * FROM test WHERE test_col1 = %s;",
                ],
                [("Testing1", "Testing2"), ("Testing1",)],
                False,
                True,
            ),
            (
                ["DELETE FROM test WHERE test_col1 = %s;", "SELECT * FROM test WHERE test_col1 = %s;"],
                [("Testing1",), ("Testing1",)],
                False,
                False,
            ),
        ],
    )
    def test_execute_sql_parametrized(self, sql_queries, query_params, expected_value, expect_data):
        """Tests PostgresDatabaseHandler.execute_sql_parametrized()."""

        assert (
            self.database_handler.execute_sql_parametrized(sql_queries=sql_queries, query_params=query_params)
            == expected_value
        )
        data = self.database_handler.cursor.fetchone()

        if expect_data:
            assert data["test_col1"] == "Testing1"
            assert data["test_col2"] == "Testing2"

        else:
            assert data is None

    @pytest.mark.parametrize(
        "sql_queries,query_params,expected_value,expect_data",
        [
            ("SELECT * FROM test WHERE test_col1 = 'Testing1';", None, False, False),
            (
                [
                    "INSERT INTO test (test_col1, test_col2) VALUES (%s, %s);",
                    "SELECT * FROM test WHERE test_col1 = %s;",
                ],
                [("Testing1", "Testing2"), ("Testing1",)],
                False,
                True,
            ),
            (
                ["DELETE FROM test WHERE test_col1 = 'Testing1';", "SELECT * FROM test WHERE test_col1 = 'Testing1';"],
                None,
                False,
                False,
            ),
            ("SELECT * FROM test WHERE test_col1 = %s;", ("Testing1",), False, False),
            (
                [
                    "INSERT INTO test (test_col1, test_col2) VALUES ('Testing1', 'Testing2');",
                    "SELECT * FROM test WHERE test_col1 = 'Testing1';",
                ],
                None,
                False,
                True,
            ),
            (
                ["DELETE FROM test WHERE test_col1 = %s;", "SELECT * FROM test WHERE test_col1 = %s;"],
                [("Testing1",), ("Testing1",)],
                False,
                False,
            ),
        ],
    )
    def test_execute_sql(self, sql_queries, query_params, expected_value, expect_data):
        """Tests PostgresDatabaseHandler.execute_sql()."""

        assert self.database_handler.execute_sql(sql_queries=sql_queries, query_params=query_params) == expected_value
        data = self.database_handler.cursor.fetchone()

        if expect_data:
            assert data["test_col1"] == "Testing1"
            assert data["test_col2"] == "Testing2"

        else:
            assert data is None
