import logging
import schedule
import time

from fedpipeline.api_handler import get_token, fetch_data_from_api
from fedpipeline.db_handler import insert_records
from fedpipeline.config import API_CONFIG


def run_entity_job(name, url, format_fn, query):
    try:
        token = get_token()
        if not token:
            logging.error(f"Skipping {name} job: Missing token.")
            return

        items = fetch_data_from_api(url, token)
        if items is None:
            logging.error(f"Skipping {name} job: API returned None.")
            return

        formatted = [format_fn(i) for i in items]
        insert_records(query, formatted, name)
        logging.info(f"{name} job completed successfully. {len(formatted)} records inserted.")

    except Exception as e:
        logging.exception(f"Error occurred during {name} job: {str(e)}")


def job():
    logging.info("Starting scheduled job...")

    try:
        token = get_token()
        if not token:
            logging.error("Job aborted: Missing token.")
            return

        from fedpipeline.jobs import (
            process_integration_users,
            process_schools,
            process_readings,
            process_units,
            process_teaching_sessions,
            process_reading_lists,
            process_reading_list_items,
            process_reading_list_usage,
            process_reading_list_item_usage,
            process_reading_utilisation,
            process_unit_offerings
        )

        # Wrap each call in try-except to isolate failures
        for process_fn in [
            process_integration_users,
            process_schools,
            process_readings,
            process_units,
            process_teaching_sessions,
            process_reading_lists,
            process_reading_list_items,
            process_reading_list_usage,
            process_reading_list_item_usage,
            process_reading_utilisation,
            process_unit_offerings
        ]:
            try:
                process_fn(token)
                logging.info(f"{process_fn.__name__} execution completed.")
            except Exception as e:
                logging.exception(f"Error in {process_fn.__name__}: {str(e)}")

    except Exception as e:
        logging.exception(f"Unexpected error in job(): {str(e)}")


def start_scheduler():
    try:
        schedule.every(1).minutes.do(job)
        logging.info("Scheduler started. Waiting for job trigger...")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logging.exception(f"Scheduler crashed: {str(e)}")
