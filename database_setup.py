import os

from database.execute_sql import PostgresDatabaseHandler

us_txt_filepath = os.getcwd() + "/database/US.txt"

create_places_table_query = """CREATE TABLE IF NOT EXISTS places (
    country_code CHAR(2),
    postal_code VARCHAR(5),
    place_name VARCHAR(180),
    admin_name1 VARCHAR(100),
    admin_code1 VARCHAR(20),
    admin_name2 VARCHAR(100),
    admin_code2 VARCHAR(20),
    admin_name3 VARCHAR(100),
    admin_code3 VARCHAR(20),
    latitude NUMERIC,
    longitude NUMERIC,
    accuracy VARCHAR(1),
    UNIQUE (postal_code, latitude, longitude)
);"""

create_users_table_query = """CREATE TABLE IF NOT EXISTS users (
    phone_number VARCHAR(20),
    default_latitude NUMERIC,
    default_longitude NUMERIC,
    current_latitude NUMERIC,
    current_longitude NUMERIC
);"""

create_test_table_query = """CREATE TABLE IF NOT EXISTS test (
    test_col1 VARCHAR(10),
    test_col2 VARCHAR(10)
);"""

copy_us_txt_file_query = f"COPY places FROM '{us_txt_filepath}' WITH (FORMAT text, DELIMITER E'\t');"

sql_queries = [create_places_table_query, create_users_table_query, create_test_table_query, copy_us_txt_file_query]
postgres_handler = PostgresDatabaseHandler()

if postgres_handler.execute_sql(sql_queries, close_connection=True):
    raise RuntimeError("Error: There was an error configuring the database!")
