import pyodbc
import logging
from fedpipeline.config import DB_CONFIG

# Construct the database connection string
conn_str = (
    f"DRIVER={{{DB_CONFIG['DRIVER']}}};"
    f"SERVER={DB_CONFIG['SERVER']};"
    f"DATABASE={DB_CONFIG['DATABASE']};"
    f"UID={DB_CONFIG['UID']};"
    f"PWD={DB_CONFIG['PWD']}"
)

def insert_records(query, records, entity_name):
    if not records:
        logging.warning(f"No {entity_name} records to insert.")
        return

    logging.info(f"Inserting {len(records)} {entity_name} records to DB.")
    
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            for record in records:
                try:
                    cursor.execute(query, record)
                except Exception as e:
                    logging.error(f"Error executing query for record with ID: {record[0]} – {e}")
            conn.commit()
        logging.info(f"{len(records)} {entity_name} records insertion ended.")
    except Exception as e:
        logging.error(f"Failed to connect to database or insert {entity_name} records: {e}")
