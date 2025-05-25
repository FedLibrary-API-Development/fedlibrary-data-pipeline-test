import pytest
from unittest.mock import patch, Mock
from fedpipeline import api_handler

@patch("fedpipeline.api_handler.requests.post")
def test_get_token_success(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.headers.get.return_value = "Bearer mock_token"
    mock_post.return_value = mock_response

    token = api_handler.get_token()
    assert token == "Bearer mock_token"


