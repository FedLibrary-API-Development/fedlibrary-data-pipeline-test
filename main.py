"""
-------------------------------------------------------------------------------
Author: Tharu Geethz
Created: 2025-04-27
Description:
    Scheduled script to fetch data from the eReserve API, transform it,
    and insert into SQL Server database tables while preserving
    foreign key constraints. Jobs are run every minute.
-------------------------------------------------------------------------------
"""


import requests
import pyodbc
import schedule
import time
import logging
from datetime import datetime
from config import API_URL, DB_CONFIG
import logger

# ------------------------- Configuration -------------------------

# Connection string
conn_str = (
    f"DRIVER={{{DB_CONFIG['DRIVER']}}};"
    f"SERVER={DB_CONFIG['SERVER']};"
    f"DATABASE={DB_CONFIG['DATABASE']};"
    f"UID={DB_CONFIG['UID']};"
    f"PWD={DB_CONFIG['PWD']}"
)

# API Endpoints
LOGIN_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/users/login"
SCHOOLS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/schools"
READINGS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/readings"
UNITS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/units"
TEACHING_SESSIONS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/teaching-sessions"
READING_LISTS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-lists"
READING_LIST_ITEMS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-list-items"

# ------------------------- Utility Functions -------------------------

def get_token():
    payload = {
        "email": "admin@example.edu",
        "password": "anypassword"
    }
    try:
        response = requests.post(LOGIN_URL, json=payload)
        response.raise_for_status()
        token = response.headers.get("Authorization")
        if not token:
            logging.error("Authorization token not found.")
        return token
    except Exception as e:
        logging.error(f"Failed to login and fetch token: {e}")
        return None

def fetch_data_from_api(url, token):
    try:
        headers = {"Authorization": token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("items", [])
    except Exception as e:
        logging.error(f"Failed to fetch data from {url}: {e}")
        return []

def insert_records(query, records, entity_name):
    logging.info(f"Inserting {len(records)} {entity_name} records to DB.")
    if not records:
        logging.warning(f"No {entity_name} records to insert.")
        return
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            # cursor.fast_executemany = True  # Uncomment for faster bulk inserts
            # cursor.executemany(query, records)

            for record in records:
                cursor.execute(query, record)
            conn.commit()
        
        logging.info(f"{len(records)} {entity_name} records inserted successfully.")
    except Exception as e:
        logging.error(f"Failed to insert {entity_name} records: {e}")

# ------------------------- Processing and Inserting Data -------------------------

def process_schools(token):
    schools = fetch_data_from_api(SCHOOLS_URL, token)
    formatted = [
        (item.get("id"), item.get("name"))
        for item in schools
    ]
    query = """
        INSERT INTO School (ereserve_id, name)
        VALUES (?, ?)
    """
    insert_records(query, formatted, "School")

def process_readings(token):
    readings = fetch_data_from_api(READINGS_URL, token)
    logging.info(f"Fetched {len(readings)} Reading records from API.")
    formatted = [
        (
            item.get("id"),
            item.get("reading_title"),
            item.get("genre"),
            item.get("source_document_title"),
            item.get("article_number"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in readings
    ]
    query = """
        INSERT INTO Reading (ereserve_id, reading_title, genre, source_document_title, article_number, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "Reading")

def process_units(token):
    units = fetch_data_from_api(UNITS_URL, token)
    formatted = [
        (item.get("id"), item.get("code"), item.get("name"))
        for item in units
    ]
    query = """
        INSERT INTO Unit (ereserve_id, code, name)
        VALUES (?, ?, ?)
    """
    insert_records(query, formatted, "Unit")

def process_teaching_sessions(token):
    teaching_sessions = fetch_data_from_api(TEACHING_SESSIONS_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("name"),
            item.get("start_date"),
            item.get("end_date"),
            item.get("archived"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in teaching_sessions
    ]
    query = """
        INSERT INTO TeachingSession (ereserve_id, name, start_date, end_date, archived, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "TeachingSession")

def process_reading_lists(token):
    reading_lists = fetch_data_from_api(READING_LISTS_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("unit_id"),
            item.get("teaching_session_id"),
            item.get("name"),
            item.get("duration"),
            item.get("start_date"),
            item.get("end_date"),
            item.get("hidden"),
            item.get("usage_count"),
            item.get("item_count"),
            item.get("approved_item_count"),
            item.get("deleted"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in reading_lists
    ]
    query = """
        INSERT INTO ReadingList (ereserve_id, unit_id, teaching_session_id, name, duration, start_date, end_date, hidden, usage_count, item_count, approved_item_count, deleted, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingList")

def process_reading_list_items(token):
    reading_list_items = fetch_data_from_api(READING_LIST_ITEMS_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("list_id"),
            item.get("reading_id"),
            item.get("status"),
            item.get("hidden"),
            item.get("reading_utilisations_count"),
            item.get("reading_importance"),
            item.get("usage_count"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in reading_list_items
    ]
    query = """
        INSERT INTO ReadingListItem (ereserve_id, list_id, reading_id, status, hidden, reading_utilisations_count, reading_importance, usage_count, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingListItem")

# ------------------------- Scheduled Job -------------------------

def job():
    logging.info("Starting scheduled job...")
    token = get_token()
    if token:
        process_schools(token)
        process_readings(token)
        process_units(token)
        process_teaching_sessions(token)
        process_reading_lists(token)
        process_reading_list_items(token)
    else:
        logging.error("Job aborted due to missing token.")

# ------------------------- Scheduler -------------------------

schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    logging.info("Scheduler started. Waiting for job trigger...")
    while True:
        schedule.run_pending()
        time.sleep(1)
