import psycopg2
import psycopg2.extras

from src.utilities import PostgresAuth


class PostgresDatabaseHandler:
    def __init__(self):
        self.postgres_auth = PostgresAuth()
        self.database = None
        self.cursor = None
        self.connect_to_database()

    def connect_to_database(self):
        """Method to connect to the Postgres database.

        :return: True if failure; False otherwise
        """

        self.database = psycopg2.connect(**vars(self.postgres_auth))
        self.cursor = self.database.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # self.database.closed only returns 0 is database connection is open
        return self.database.closed != 0

    def close_database_connection(self):
        """Method to close the database connection and the cursor object.

        :return: True if failure; False otherwise
        """

        if not self.database.closed:
            self.cursor.close()
            self.database.close()

        # self.database.closed only returns 0 is database connection is open
        return self.database.closed == 0

    def execute_simple_sql(self, sql_queries, close_connection=False):
        """
        Use to execute simple, non-parametrized SQL queries.

        :param sql_queries: SQL query string or List of SQL query strings
        :param close_connection: True to close the database connections after successful execution; False to keep
                                 connection open
        :return: True if failure; False otherwise
        """

        try:
            if not isinstance(sql_queries, list):
                sql_queries = [sql_queries]

            if not all(isinstance(sql_query, str) for sql_query in sql_queries):
                raise RuntimeError("Error: Each query must be of type str!")

            if self.database.closed:
                if self.connect_to_database():
                    raise RuntimeError("Error: Could not connect to the database!")

            for sql_query in sql_queries:
                self.cursor.execute(sql_query)

            # Commit the changes to the database
            self.database.commit()

            if close_connection:
                if self.close_database_connection():
                    print("Warning: Could not close database connection!")

            return False

        except Exception as e:
            print(f"Error: Something went wrong accessing the database: {str(e)}")
            return True

    def execute_sql_parametrized(self, sql_queries, query_params, close_connection=False):
        """
        Use to execute parametrized SQL queries. A parametrized query is of the form:

            "SELECT * FROM my_table WHERE name = %s AND age = %s"

        Where the %s are placeholders. This query will take in two parameters passed in as a tuple (name, age).

        :param sql_queries: SQL query string or List of SQL query strings
        :param query_params: Tuple of SQL parameters, or List of tuples of SQL parameters
        :param close_connection: True to close the database connections after successful execution; False to keep
                                 connection open
        :return: True if Failure; False otherwise
        """

        try:
            if not isinstance(sql_queries, list):
                sql_queries = [sql_queries]

            if not all(isinstance(sql_query, str) for sql_query in sql_queries):
                raise RuntimeError("Error: Each query must be of type str!")

            if not isinstance(query_params, list):
                query_params = [query_params]

            if not all(isinstance(params, tuple) for params in query_params):
                raise RuntimeError("Error: Each set of query params must be of type tuple!")

            if len(sql_queries) != len(query_params):
                raise RuntimeError("Number of SQL queries does not match the number of query parameters given.")

            if self.database.closed:
                if self.connect_to_database():
                    raise RuntimeError("Error: Could not connect to the database!")

            for sql_query, params in zip(sql_queries, query_params):
                self.cursor.execute(sql_query, params)

            # Commit the changes to the database
            self.database.commit()

            if close_connection:
                if self.close_database_connection():
                    print("Warning: Could not close database connection!")

            return False

        except Exception as e:
            print(f"Error: Something went wrong accessing the database: {str(e)}")
            return True

    def execute_sql(self, sql_queries, query_params=None, close_connection=False):
        """
        Driver function to execute SQL queries, whether parametrized or not.

        :param sql_queries: SQL query string or List of SQL query strings
        :param query_params: Tuple of SQL parameters, or List of tuples of SQL parameters
        :param close_connection: True to close the database connections after successful execution; False to keep
                                 connection open
        :return: True if Failure; False otherwise
        """

        if not query_params:
            return self.execute_simple_sql(sql_queries, close_connection)

        else:
            return self.execute_sql_parametrized(sql_queries, query_params, close_connection)
