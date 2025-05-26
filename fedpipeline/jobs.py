import logging
from fedpipeline.api_handler import fetch_data_from_api
from fedpipeline.db_handler import insert_records
from fedpipeline.config import API_CONFIG


def process_integration_users(token):
    try:
        users = fetch_data_from_api(API_CONFIG["INTEGRATION_USERS_URL"], token)
        if not users:
            logging.warning("No IntegrationUser data fetched.")
            return
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
            ) for item in users
        ]
        query = """
            INSERT INTO IntegrationUser (
                ereserve_id, identifier, roles, first_name, last_name, email,
                lti_consumer_user_id, lti_lis_person_sourcedid, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "IntegrationUser")
    except Exception as e:
        logging.error(f"Error processing IntegrationUser data: {e}")


def process_schools(token):
    try:
        schools = fetch_data_from_api(API_CONFIG["SCHOOLS_URL"], token)
        if not schools:
            logging.warning("No School data fetched.")
            return
        formatted = [(item.get("id"), item.get("name")) for item in schools]
        query = "INSERT INTO School (ereserve_id, name) VALUES (?, ?)"
        insert_records(query, formatted, "School")
    except Exception as e:
        logging.error(f"Error processing School data: {e}")


def process_readings(token):
    try:
        readings = fetch_data_from_api(API_CONFIG["READINGS_URL"], token)
        if not readings:
            logging.warning("No Reading data fetched.")
            return
        formatted = [
            (
                item.get("id"),
                item.get("reading_title"),
                item.get("genre"),
                item.get("source_document_title"),
                item.get("article_number"),
                item.get("created_at"),
                item.get("updated_at")
            ) for item in readings
        ]
        query = """
            INSERT INTO Reading (
                ereserve_id, reading_title, genre, source_document_title,
                article_number, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "Reading")
    except Exception as e:
        logging.error(f"Error processing Reading data: {e}")


def process_units(token):
    try:
        units = fetch_data_from_api(API_CONFIG["UNITS_URL"], token)
        if not units:
            logging.warning("No Unit data fetched.")
            return
        formatted = [(item.get("id"), item.get("code"), item.get("name")) for item in units]
        query = "INSERT INTO Unit (ereserve_id, code, name) VALUES (?, ?, ?)"
        insert_records(query, formatted, "Unit")
    except Exception as e:
        logging.error(f"Error processing Unit data: {e}")


def process_unit_offerings(token):
    try:
        offerings = fetch_data_from_api(API_CONFIG["UNIT_OFFERINGS_URL"], token)
        if not offerings:
            logging.warning("No UnitOffering data fetched.")
            return
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
            ) for item in offerings
        ]
        query = """
            INSERT INTO UnitOffering (
                ereserve_id, unit_id, reading_list_id, source_unit_code,
                source_unit_name, source_unit_offering, result,
                list_publication_method, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "UnitOffering")
    except Exception as e:
        logging.error(f"Error processing UnitOffering data: {e}")


def process_teaching_sessions(token):
    try:
        sessions = fetch_data_from_api(API_CONFIG["TEACHING_SESSIONS_URL"], token)
        if not sessions:
            logging.warning("No TeachingSession data fetched.")
            return
        formatted = [
            (
                item.get("id"),
                item.get("name"),
                item.get("start_date"),
                item.get("end_date"),
                item.get("archived"),
                item.get("created_at"),
                item.get("updated_at")
            ) for item in sessions
        ]
        query = """
            INSERT INTO TeachingSession (
                ereserve_id, name, start_date, end_date,
                archived, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "TeachingSession")
    except Exception as e:
        logging.error(f"Error processing TeachingSession data: {e}")


def process_reading_lists(token):
    try:
        lists = fetch_data_from_api(API_CONFIG["READING_LISTS_URL"], token)
        if not lists:
            logging.warning("No ReadingList data fetched.")
            return
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
            ) for item in lists
        ]
        query = """
            INSERT INTO ReadingList (
                ereserve_id, unit_id, teaching_session_id, name, duration,
                start_date, end_date, hidden, usage_count, item_count,
                approved_item_count, deleted, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "ReadingList")
    except Exception as e:
        logging.error(f"Error processing ReadingList data: {e}")


def process_reading_list_items(token):
    try:
        items = fetch_data_from_api(API_CONFIG["READING_LIST_ITEMS_URL"], token)
        if not items:
            logging.warning("No ReadingListItem data fetched.")
            return
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
            ) for item in items
        ]
        query = """
            INSERT INTO ReadingListItem (
                ereserve_id, list_id, reading_id, status, hidden,
                reading_utilisations_count, reading_importance,
                usage_count, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "ReadingListItem")
    except Exception as e:
        logging.error(f"Error processing ReadingListItem data: {e}")


def process_reading_list_usage(token):
    try:
        usages = fetch_data_from_api(API_CONFIG["READING_LIST_USAGE_URL"], token)
        if not usages:
            logging.warning("No ReadingListUsage data fetched.")
            return
        formatted = [
            (
                item.get("id"),
                item.get("list_id"),
                item.get("integration_user_id"),
                item.get("item_usage_count"),
                item.get("list_publication_method"),
                item.get("created_at"),
                item.get("updated_at")
            ) for item in usages
        ]
        query = """
            INSERT INTO ReadingListUsage (
                ereserve_id, list_id, integration_user_id,
                item_usage_count, list_publication_method,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "ReadingListUsage")
    except Exception as e:
        logging.error(f"Error processing ReadingListUsage data: {e}")


def process_reading_list_item_usage(token):
    try:
        usages = fetch_data_from_api(API_CONFIG["READING_LIST_ITEM_USAGE_URL"], token)
        if not usages:
            logging.warning("No ReadingListItemUsage data fetched.")
            return
        formatted = [
            (
                item.get("id"),
                item.get("item_id"),
                item.get("list_usage_id"),
                item.get("integration_user_id"),
                item.get("utilisation_count"),
                item.get("created_at"),
                item.get("updated_at")
            ) for item in usages
        ]
        query = """
            INSERT INTO ReadingListItemUsage (
                ereserve_id, item_id, list_usage_id,
                integration_user_id, utilisation_count,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "ReadingListItemUsage")
    except Exception as e:
        logging.error(f"Error processing ReadingListItemUsage data: {e}")


def process_reading_utilisation(token):
    try:
        utilisations = fetch_data_from_api(API_CONFIG["READING_UTILISATION_URL"], token)
        if not utilisations:
            logging.warning("No ReadingUtilisation data fetched.")
            return
        formatted = [
            (
                item.get("id"),
                item.get("integration_user_id"),
                item.get("item_id"),
                item.get("item_usage_id"),
                item.get("created_at"),
                item.get("updated_at")
            ) for item in utilisations
        ]
        query = """
            INSERT INTO ReadingUtilisation (
                ereserve_id, integration_user_id, item_id,
                item_usage_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        insert_records(query, formatted, "ReadingUtilisation")
    except Exception as e:
        logging.error(f"Error processing ReadingUtilisation data: {e}")
