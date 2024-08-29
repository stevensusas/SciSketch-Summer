import pymysql
import pandas as pd
import time
import logging

class MySQLConnector:
    def __init__(self):
        """
        Initialize the MySQLConnector object and establish a connection to the MySQL database.
        """
        self.host = "scisketch-finetuning.cha8ies4obs2.us-east-1.rds.amazonaws.com"
        self.user = "admin"
        self.password = "12345678"  # Replace with your actual password
        self.database = "scisketch"
        self.port = 3306
        self.ssl_ca = "global-bundle.pem"  # Update with the actual path if needed
        self.connection = None
        self.connect()

    def connect(self):
        """Establishes the connection to the MySQL database."""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database,
                port=self.port,
                ssl_ca=self.ssl_ca
            )
            print("Connected to the MySQL database.")
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def close_connection(self):
        """Closes the connection to the MySQL database."""
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def upload_dataframe(self, df, table_name, max_retries=3, delay=5):
        """
        Uploads a Pandas DataFrame to a new table in the MySQL database, allowing NULL values.
        :param df: Pandas DataFrame to upload
        :param table_name: Name of the new table to create in the database
        :param max_retries: Maximum number of retry attempts
        :param delay: Delay between retries in seconds
        """
        for attempt in range(max_retries):
            try:
                with self.connection.cursor() as cursor:
                    # Check if table exists
                    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
                    table_exists = cursor.fetchone() is not None

                    if not table_exists:
                        # Generate the SQL statement for creating a table
                        columns = ', '.join(f"`{col}` TEXT" for col in df.columns)
                        create_table_sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns});"
                        cursor.execute(create_table_sql)
                    else:
                        # If table exists, drop it and recreate
                        cursor.execute(f"DROP TABLE `{table_name}`;")
                        columns = ', '.join(f"`{col}` TEXT" for col in df.columns)
                        create_table_sql = f"CREATE TABLE `{table_name}` ({columns});"
                        cursor.execute(create_table_sql)

                    # Prepare the SQL statement for inserting rows
                    placeholders = ', '.join(['%s'] * len(df.columns))
                    insert_sql = f"INSERT INTO `{table_name}` VALUES ({placeholders});"

                    # Insert DataFrame rows into the table
                    for _, row in df.iterrows():
                        values = [None if pd.isna(value) else value for value in row]
                        cursor.execute(insert_sql, tuple(values))

                    # Commit the transaction
                    self.connection.commit()
                    print(f"DataFrame uploaded successfully to the table {table_name}.")
                    return
            except pymysql.MySQLError as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    self.connect()  # Reconnect to the database
                else:
                    print("Max retries reached. Upload failed.")
                    raise

    def list_tables(self):
        """
        Retrieves and returns a list of all table names in the connected database.
        :return: List of table names
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                return table_names
        except pymysql.MySQLError as e:
            print(f"Error fetching table names: {e}")
            return []

    def execute_query(self, query):
        """
        Executes a given SQL query and returns the results.
        :param query: SQL query to execute
        :return: List of tuples containing the query results
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            return []

    def preview_table(self, table_name, limit=5):
        """
        Previews the content of a specified table.
        :param table_name: Name of the table to preview
        :param limit: Number of rows to preview, default is 5
        :return: Pandas DataFrame containing the preview of the table
        """
        try:
            query = f"SELECT * FROM `{table_name}` LIMIT {limit};"
            df = pd.read_sql(query, self.connection)
            return df
        except pymysql.MySQLError as e:
            print(f"Error previewing table `{table_name}`: {e}")
            return pd.DataFrame()

    def fetch_table(self, table_name):
        """
        Retrieves the entire content of a specified table.
        :param table_name: Name of the table to retrieve
        :return: Pandas DataFrame containing the entire table
        """
        try:
            query = f"SELECT * FROM `{table_name}`;"
            df = pd.read_sql(query, self.connection)
            return df
        except pymysql.MySQLError as e:
            print(f"Error fetching table `{table_name}`: {e}")
            return pd.DataFrame()

    def table_exists(self, table_name):
        """
        Checks if a table exists in the database.
        :param table_name: Name of the table to check
        :return: Boolean indicating whether the table exists
        """
        try:
            with self.connection.cursor() as cursor:
                query = f"SHOW TABLES LIKE '{table_name}'"
                cursor.execute(query)
                result = cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            print(f"Error checking if table exists: {e}")
            return False

    def __del__(self):
        """Ensures the connection is closed when the object is deleted."""
        self.close_connection()