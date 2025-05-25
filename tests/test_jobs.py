import pytest
from unittest.mock import patch
from fedpipeline import jobs

@pytest.fixture
def dummy_token():
    return "fake_token"

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

