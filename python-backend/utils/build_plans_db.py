import sqlite3
import os

# generated using gemini

def build_roaming_plans_db(db_name="roaming_plans.db"):
    """
    Builds an SQLite database and creates a 'plans' table
    with 'customer_name', 'phone_number', 'roaming_plan', 'timestamp' fields.

    Args:
        db_name (str): The name of the SQLite database file.
    """
    conn = None # Initialize connection to None
    try:
        # Connect to SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        print(f"Connected to database: {db_name}")

        
        # DROP TABLE if it exists; trigger manually to be safe
        # cursor.execute('DROP TABLE IF EXISTS plans')
        
        # SQL statement to create the table if it does not exist
        # 'IF NOT EXISTS' is crucial for preventing errors if the table already exists
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS plans (
            customer_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            roaming_plan TEXT DEFAULT 'None', 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            
        );
        """

        cursor.execute(create_table_sql)
        conn.commit() # Commit the changes to the database

        print("Table 'plans' checked/created successfully.")

        # Optional: Verify table creation by listing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plans';")
        if cursor.fetchone():
            print("Verification: 'plans' table exists.")
        else:
            print("Verification: 'plans' table DOES NOT exist (this should not happen).")

    except sqlite3.Error as e:
        print(f"An SQLite error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# --- How to use the script ---
if __name__ == "__main__":
    # Define the database file name
    database_file = os.getcwd() + "/python-backend/roaming_plans.db"

    # Clean up previous database file for fresh start (optional, for testing)
    # if os.path.exists(database_file):
    #     os.remove(database_file)
    #     print(f"Removed existing database file: {database_file}")

    # Call the function to build the database and table
    build_roaming_plans_db(database_file)


    # You can now connect to the database and insert/query data
    # Example of inserting data (optional)
    # conn = sqlite3.connect(database_file)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO plans (customer_name, phone_number, roaming_plan) VALUES (?, ?, ?)", ("Alice", "1234567890", "Europe 5GB"))
    # cursor.execute("INSERT INTO plans (customer_name, phone_number, roaming_plan) VALUES (?, ?, ?)", ("Bob", "0987654321", "Asia Unlimited"))
    # conn.commit()
    # print("\nInserted example data.")
    #
    # cursor.execute("SELECT * FROM plans")
    # print("Current data in plans:")
    # for row in cursor.fetchall():
    #     print(row)
    # conn.close()
