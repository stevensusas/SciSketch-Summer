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

    def drop_duplicates_in_doi(self):
        """
        Drops duplicates in the 'doi' column for all tables in the database, handling cases where 'id' is not present.
        """
        try:
            # Fetch all table names
            tables = self.list_tables()

            for table in tables:
                print(f"Processing table: {table}")
                
                # Check if the 'doi' column exists in the current table
                query = f"""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                AND column_name = 'doi'
                """
                result = self.execute_query(query)

                if result[0][0] > 0:
                    # Check if the 'id' column exists in the table
                    query = f"""
                    SELECT COUNT(*) 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' 
                    AND column_name = 'id'
                    """
                    id_exists = self.execute_query(query)[0][0] > 0
                    
                    if id_exists:
                        # If the 'id' column exists, use it to drop duplicates
                        print(f"Dropping duplicates in 'doi' column for table {table} using 'id'...")

                        # Step 1: Identify duplicate 'doi' values and the minimum 'id' for each group
                        duplicate_query = f"""
                        SELECT id
                        FROM `{table}`
                        WHERE id NOT IN (
                            SELECT MIN(id)
                            FROM `{table}`
                            GROUP BY doi
                            HAVING COUNT(doi) > 1
                        );
                        """
                        ids_to_delete = self.execute_query(duplicate_query)

                        # Step 2: Delete the duplicates based on identified 'id's
                        if ids_to_delete:
                            ids_to_delete_str = ",".join([str(row[0]) for row in ids_to_delete])
                            delete_query = f"DELETE FROM `{table}` WHERE id IN ({ids_to_delete_str});"
                            self.execute_query(delete_query)
                            print(f"Duplicates dropped in table: {table}")
                        else:
                            print(f"No duplicates found in table: {table}")

                    else:
                        # If the 'id' column doesn't exist, we'll handle it by identifying duplicates without 'id'
                        print(f"Dropping duplicates in 'doi' column for table {table} without 'id'...")

                        # Step 1: Create a temporary table with unique DOI records
                        temp_table_name = f"{table}_temp"
                        create_temp_table = f"""
                        CREATE TEMPORARY TABLE `{temp_table_name}` AS
                        SELECT * FROM `{table}`
                        WHERE doi IN (
                            SELECT doi FROM `{table}`
                            GROUP BY doi
                            HAVING COUNT(doi) = 1
                        );
                        """
                        self.execute_query(create_temp_table)

                        # Step 2: Delete all records from the original table
                        delete_all = f"DELETE FROM `{table}`;"
                        self.execute_query(delete_all)

                        # Step 3: Insert the unique records back into the original table
                        insert_unique = f"INSERT INTO `{table}` SELECT * FROM `{temp_table_name}`;"
                        self.execute_query(insert_unique)

                        print(f"Duplicates dropped in table: {table}")

                else:
                    print(f"Skipping table {table}, no 'doi' column found.")

        except pymysql.MySQLError as e:
            print(f"Error dropping duplicates: {e}")



    def count_true_in_graphical_abstract(self):
        """
        For all tables in the database, list the number of rows where the GraphicalAbstract column contains TRUE,
        as well as the total count across all tables.
        """
        try:
            tables = self.list_tables()  # Get all table names
            total_true_count = 0  # To store the total count of TRUE across all tables

            # Iterate through each table
            for table in tables:
                # Check if the table contains a 'GraphicalAbstract' column
                query = f"""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                AND column_name = 'GraphicalAbstract'
                """
                result = self.execute_query(query)

                if result[0][0] > 0:  # If 'GraphicalAbstract' column exists
                    # Count the number of TRUE values in the 'GraphicalAbstract' column
                    query = f"""
                    SELECT COUNT(*) 
                    FROM `{table}` 
                    WHERE GraphicalAbstract = TRUE;
                    """
                    count_result = self.execute_query(query)
                    count_true = count_result[0][0]
                    total_true_count += count_true
                    print(f"Table: {table} | Count of TRUE in 'GraphicalAbstract': {count_true}")
                else:
                    print(f"Table {table} does not have a 'GraphicalAbstract' column. Skipping...")

            print(f"Total number of TRUE values across all tables: {total_true_count}")
            return total_true_count

        except pymysql.MySQLError as e:
            print(f"Error counting TRUE values in 'GraphicalAbstract': {e}")
    
    def check_for_duplicate_doi(self):
        """
        Checks all tables in the database and returns the names of tables that contain duplicate entries in the 'doi' column.
        :return: List of table names that contain duplicate 'doi' entries
        """
        tables_with_duplicates = []  # To store table names with duplicate 'doi' values
        try:
            # Fetch all table names
            tables = self.list_tables()

            # Iterate through each table and check if it has duplicate entries in the 'doi' column
            for table in tables:
                # Check if the 'doi' column exists in the table
                query = f"""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_name = '{table}'
                AND column_name = 'doi'
                AND table_schema = '{self.database}';
                """
                result = self.execute_query(query)

                if result[0][0] > 0:  # If the 'doi' column exists
                    # Query to check for duplicates in the 'doi' column
                    duplicate_query = f"""
                    SELECT doi
                    FROM `{table}`
                    GROUP BY doi
                    HAVING COUNT(doi) > 1;
                    """
                    duplicates = self.execute_query(duplicate_query)

                    if duplicates:
                        tables_with_duplicates.append(table)
                        print(f"Table {table} contains duplicate 'doi' entries.")
                else:
                    print(f"Table {table} does not contain a 'doi' column.")

            return tables_with_duplicates

        except pymysql.MySQLError as e:
            print(f"Error checking for duplicate 'doi' entries: {e}")
            return []


    def __del__(self):
        """Ensures the connection is closed when the object is deleted."""
        self.close_connection()

if __name__ == "__main__":
    # Initialize the MySQLConnector
    db = MySQLConnector()
    db.count_true_in_graphical_abstract()