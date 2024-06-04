import psycopg2

def execute_sql_query_insert(conn_str, sql_query, params=None):

    # Connect to the database
    connection = psycopg2.connect(conn_str)
    # Create a cursor
    cursor = connection.cursor()

    # Execute the SQL query with parameters
    if params:
        cursor.execute(sql_query, params)
    else:
        cursor.execute(sql_query)

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

def execute_sql_query_get(conn_str, sql_query, params=None):

    # Connect to the database
    connection = psycopg2.connect(conn_str)
    # Create a cursor
    cursor = connection.cursor()

    # Execute the SQL query with parameters
    if params:
        cursor.execute(sql_query, params)
    else:
        cursor.execute(sql_query)

    # Get the query result
    result = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return result  # Return the query result



# Database connection string
host = 'localhost'
port = '5432'
database_name = 'sclad'
username = 'postgres'
password = '25122002'

conn_str = f"host='{host}' port='{port}' dbname='{database_name}' user='{username}' password='{password}'"
