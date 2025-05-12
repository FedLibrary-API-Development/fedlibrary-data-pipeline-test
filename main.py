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
INTEGRATION_USERS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/integration-users"
READINGS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/readings"
UNITS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/units"
UNIT_OFFERINGS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/unit-offerings"
TEACHING_SESSIONS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/teaching-sessions"
READING_LISTS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-lists"
READING_LIST_USAGE_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-list-usages"
READING_LIST_ITEMS_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-list-items"
READING_LIST_ITEM_USAGE_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-list-item-usages"
READING_UTILISATION_URL = "https://teambmockapi-569115112148.us-central1.run.app/api/v1/reading-utilisations"

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
            for record in records:
                cursor.execute(query, record)
            conn.commit()
        logging.info(f"{len(records)} {entity_name} records inserted successfully.")
    except Exception as e:
        logging.error(f"Failed to insert {entity_name} records: {e}")

# ------------------------- Processing and Inserting Data -------------------------

def process_schools(token):
    schools = fetch_data_from_api(SCHOOLS_URL, token)
    formatted = [(item.get("id"), item.get("name")) for item in schools]
    query = "INSERT INTO School (ereserve_id, name) VALUES (?, ?)"
    insert_records(query, formatted, "School")


def process_integration_users(token):
    users = fetch_data_from_api(INTEGRATION_USERS_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("identifier"),
            item.get("roles"),
            item.get("first_name"),
            item.get("last_name"),
            item.get("email"),
            item.get("lti_consumer_user_id"),
            item.get("lti_lis_person_sourcedid"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in users
    ]
    query = """
        INSERT INTO IntegrationUser (ereserve_id, identifier, roles, first_name, last_name, email,
                                     lti_consumer_user_id, lti_lis_person_sourcedid, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "IntegrationUser")


def process_readings(token):
    readings = fetch_data_from_api(READINGS_URL, token)
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
        INSERT INTO Reading (ereserve_id, reading_title, genre, source_document_title,
                             article_number, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "Reading")


def process_units(token):
    units = fetch_data_from_api(UNITS_URL, token)
    formatted = [(item.get("id"), item.get("code"), item.get("name")) for item in units]
    query = "INSERT INTO Unit (ereserve_id, code, name) VALUES (?, ?, ?)"
    insert_records(query, formatted, "Unit")


def process_unit_offerings(token):
    offerings = fetch_data_from_api(UNIT_OFFERINGS_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("unit_id"),
            item.get("reading_list_id"),
            item.get("source_unit_code"),
            item.get("source_unit_name"),
            item.get("source_unit_offering"),
            item.get("result"),
            item.get("list_publication_method"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in offerings
    ]
    query = """
        INSERT INTO UnitOffering (ereserve_id, unit_id, reading_list_id, source_unit_code,
                                  source_unit_name, source_unit_offering, result,
                                  list_publication_method, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "UnitOffering")


def process_teaching_sessions(token):
    sessions = fetch_data_from_api(TEACHING_SESSIONS_URL, token)
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
        for item in sessions
    ]
    query = """
        INSERT INTO TeachingSession (ereserve_id, name, start_date, end_date,
                                     archived, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "TeachingSession")


def process_reading_lists(token):
    lists = fetch_data_from_api(READING_LISTS_URL, token)
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
        for item in lists
    ]
    query = """
        INSERT INTO ReadingList (ereserve_id, unit_id, teaching_session_id, name, duration,
                                 start_date, end_date, hidden, usage_count, item_count,
                                 approved_item_count, deleted, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingList")


def process_reading_list_usage(token):
    usages = fetch_data_from_api(READING_LIST_USAGE_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("list_id"),
            item.get("integration_user_id"),
            item.get("item_usage_count"),
            item.get("list_publication_method"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in usages
    ]
    query = """
        INSERT INTO ReadingListUsage (ereserve_id, list_id, integration_user_id,
                                      item_usage_count, list_publication_method,
                                      created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingListUsage")


def process_reading_list_items(token):
    items = fetch_data_from_api(READING_LIST_ITEMS_URL, token)
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
        for item in items
    ]
    query = """
        INSERT INTO ReadingListItem (ereserve_id, list_id, reading_id, status, hidden,
                                     reading_utilisations_count, reading_importance,
                                     usage_count, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingListItem")


def process_reading_list_item_usage(token):
    usages = fetch_data_from_api(READING_LIST_ITEM_USAGE_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("item_id"),
            item.get("list_usage_id"),
            item.get("integration_user_id"),
            item.get("utilisation_count"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in usages
    ]
    query = """
        INSERT INTO ReadingListItemUsage (ereserve_id, item_id, list_usage_id,
                                          integration_user_id, utilisation_count,
                                          created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingListItemUsage")


def process_reading_utilisation(token):
    utilisations = fetch_data_from_api(READING_UTILISATION_URL, token)
    formatted = [
        (
            item.get("id"),
            item.get("integration_user_id"),
            item.get("item_id"),
            item.get("item_usage_id"),
            item.get("created_at"),
            item.get("updated_at")
        )
        for item in utilisations
    ]
    query = """
        INSERT INTO ReadingUtilisation (ereserve_id, integration_user_id, item_id,
                                        item_usage_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    insert_records(query, formatted, "ReadingUtilisation")

# ------------------------- Scheduled Job -------------------------

def job():
    logging.info("Starting scheduled job...")
    token = get_token()
    if token:
        process_integration_users(token)
        process_schools(token)
        process_readings(token)
        process_units(token)
        process_teaching_sessions(token)
        process_reading_lists(token)
        process_reading_list_items(token)
        process_reading_list_usage(token)
        process_reading_list_item_usage(token)
        process_reading_utilisation(token)
        process_unit_offerings(token)
    else:
        logging.error("Job aborted due to missing token.")

# ------------------------- Scheduler -------------------------

schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    logging.info("Scheduler started. Waiting for job trigger...")
    while True:
        schedule.run_pending()
        time.sleep(1)
