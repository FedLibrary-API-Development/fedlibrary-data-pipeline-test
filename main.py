import requests
import pyodbc
import schedule
import time
from datetime import datetime
from config import API_URL, DB_CONFIG
import logging
import logger


def fetch_data():
    url = "http://localhost:8000/api/v1/resources/"
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        
        resources = data.get("resources", [])
        records = []
        
        for item in resources:
            title = item["title"]
            description = item["description"]
            access_count = item["access_count"]
            student_count = item["student_count"]
            resource_id = item["id"]
            records.append((title, description, access_count, student_count, resource_id))

        logging.info(f"Fetched {len(records)} records from API.")
        return records
    except Exception as e:
        print(e)
        logging.error(f"Failed to fetch data: {e}")
        return None
           

def insert_data(records):
    if not records:
        logging.warning("No records to insert.")
        return
    try:
        conn_str = (
            f"DRIVER={{{DB_CONFIG['DRIVER']}}};"
            f"SERVER={DB_CONFIG['SERVER']};"
            f"DATABASE={DB_CONFIG['DATABASE']};"
            f"UID={DB_CONFIG['UID']};"
            f"PWD={DB_CONFIG['PWD']}"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = """
        INSERT INTO ResourceData (title, res_description, access_count, student_count, resource_id)
        VALUES (?, ?, ?, ?, ?)"""
        
        for record in records:
            cursor.execute(query, record)
        conn.commit()
        logging.info("Data inserted successfully.")
    except Exception as e:
        logging.error(f"Failed to insert data: {e}")
    finally:
        conn.close()

def job():
    logging.info("Starting scheduled job...")
    data = fetch_data()
    insert_data(data)

schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    logging.info("Scheduler started. Waiting for job trigger...")
    while True:
        schedule.run_pending()
        time.sleep(1)