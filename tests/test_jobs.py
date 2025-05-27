import pytest
from unittest.mock import patch
from fedpipeline import jobs

@pytest.fixture
def dummy_token():
    return "fake_token"

# ----------- Test Cases for Each Processing Function -----------

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_integration_users(mock_insert, mock_fetch, dummy_token):
    mock_fetch.return_value = [{
        "id": 1,
        "identifier": "ABC123",
        "roles": ["user"],
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "lti_consumer_user_id": "LC123",
        "lti_lis_person_sourcedid": "LIS456",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z"
    }]
    jobs.process_integration_users(dummy_token)
    mock_insert.assert_called_once()
    
@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
    #Test the process_schools function
def test_process_schools(mock_insert, mock_fetch, dummy_token):
        mock_fetch.return_value = [{"id": 2, "name": "Engineering"}]
        jobs.process_schools(dummy_token)
        mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_readings(mock_insert, mock_fetch, dummy_token):
  #  Test the process_readings function with dummy reading data.
    mock_fetch.return_value = [{
        "id": 3,
        "reading_title": "IoT Basics",
        "genre": "Tech",
        "source_document_title": "Intro to IoT",
        "article_number": "A123",
        "created_at": "2024-03-01",
        "updated_at": "2024-03-02"
    }]
    jobs.process_readings(dummy_token)
    mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_units(mock_insert, mock_fetch, dummy_token):
   # Verifies processing of units and insert call.
    mock_fetch.return_value = [{"id": 4, "code": "CS101", "name": "Intro to CS"}]
    jobs.process_units(dummy_token)
    mock_insert.assert_called_once()
    
@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_unit_offerings(mock_insert, mock_fetch, dummy_token):
    # Ensure process_unit_offerings correctly handles fetched data.
    mock_fetch.return_value = [{
        "id": 5,
        "unit_id": 4,
        "reading_list_id": 8,
        "source_unit_code": "CS101",
        "source_unit_name": "Intro to CS",
        "source_unit_offering": "2024-S1",
        "result": "Pass",
        "list_publication_method": "Manual",
        "created_at": "2024-04-01",
        "updated_at": "2024-04-02"
    }]
    jobs.process_unit_offerings(dummy_token)
    mock_insert.assert_called_once()
    
@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_teaching_sessions(mock_insert, mock_fetch, dummy_token):
    # Test for teaching session data integration.
    mock_fetch.return_value = [{
        "id": 6,
        "name": "Semester 1",
        "start_date": "2024-02-01",
        "end_date": "2024-06-01",
        "archived": False,
        "created_at": "2024-01-15",
        "updated_at": "2024-01-16"
    }]
    jobs.process_teaching_sessions(dummy_token)
    mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_reading_lists(mock_insert, mock_fetch, dummy_token):
   # Test reading list processing with expected structure.
    mock_fetch.return_value = [{
        "id": 7,
        "unit_id": 4,
        "teaching_session_id": 6,
        "name": "Week 1 Readings",
        "duration": "1 week",
        "start_date": "2024-02-01",
        "end_date": "2024-02-07",
        "hidden": False,
        "usage_count": 5,
        "item_count": 3,
        "approved_item_count": 3,
        "deleted": False,
        "created_at": "2024-01-20",
        "updated_at": "2024-01-21"
    }]
    jobs.process_reading_lists(dummy_token)
    mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_reading_list_items(mock_insert, mock_fetch, dummy_token):
   # Ensure reading list items are processed and inserted correctly.
    mock_fetch.return_value = [{
        "id": 8,
        "list_id": 7,
        "reading_id": 3,
        "status": "active",
        "hidden": False,
        "reading_utilisations_count": 10,
        "reading_importance": "high",
        "usage_count": 7,
        "created_at": "2024-01-22",
        "updated_at": "2024-01-23"
    }]
    jobs.process_reading_list_items(dummy_token)
    mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_reading_list_usage(mock_insert, mock_fetch, dummy_token):
    #Test that reading list usage entries are handled properly.
    mock_fetch.return_value = [{
        "id": 9,
        "list_id": 7,
        "integration_user_id": 1,
        "item_usage_count": 3,
        "list_publication_method": "auto",
        "created_at": "2024-01-24",
        "updated_at": "2024-01-25"
    }]
    jobs.process_reading_list_usage(dummy_token)
    mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_reading_list_item_usage(mock_insert, mock_fetch, dummy_token):
   # Confirm reading list item usage data is transformed and stored.
    mock_fetch.return_value = [{
        "id": 10,
        "item_id": 8,
        "list_usage_id": 9,
        "integration_user_id": 1,
        "utilisation_count": 2,
        "created_at": "2024-01-26",
        "updated_at": "2024-01-27"
    }]
    jobs.process_reading_list_item_usage(dummy_token)
    mock_insert.assert_called_once()

@patch("fedpipeline.jobs.fetch_data_from_api")
@patch("fedpipeline.jobs.insert_records")
def test_process_reading_utilisation(mock_insert, mock_fetch, dummy_token):
   # Test reading utilisation records are successfully processed.
    mock_fetch.return_value = [{
        "id": 11,
        "integration_user_id": 1,
        "item_id": 8,
        "item_usage_id": 10,
        "created_at": "2024-01-28",
        "updated_at": "2024-01-29"
    }]
    jobs.process_reading_utilisation(dummy_token)
    mock_insert.assert_called_once()




