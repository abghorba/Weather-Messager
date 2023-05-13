import os

from database.execute_sql import PostgresDatabaseHandler

us_txt_filepath = os.getcwd() + "/database/US.txt"

create_table_query = (
    "CREATE TABLE places IF NOT EXISTS locations "
    "( country_code CHAR(2), "
    "postal_code VARCHAR(5), "
    "place_name VARCHAR(180), "
    "admin_name1 VARCHAR(100), "
    "admin_code1 varchar(20), "
    "admin_name2 varchar(100), "
    "admin_code2 varchar(20), "
    "admin_name3 varchar(100), "
    "admin_code3 varchar(20), "
    "latitude NUMERIC, "
    "longitude NUMERIC, "
    "accuracy varchar(1) );"
)

copy_us_txt_file_query = f"COPY places FROM '{us_txt_filepath}' WITH (FORMAT text, DELIMITER E'\t', HEADER true);"

sql_queries = [create_table_query, copy_us_txt_file_query]
postgres_handler = PostgresDatabaseHandler()

if postgres_handler.execute_sql(sql_queries, close_connection=True):
    raise RuntimeError("Error: There was an error configuring the database!")
