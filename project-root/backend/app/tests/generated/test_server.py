import pytest
import requests
import json

# Fixture for the base URL of the API
@pytest.fixture
def base_url():
    """Provides the base URL for the API tests."""
    return "http://localhost:5000"

# --- Tests for /api/status Endpoint ---

# HEALING_TAG: GET_status
def test_get_status_happy_path(base_url):
    """
    Tests the happy path for the GET /api/status endpoint.
    Expects a 200 OK status and a JSON response with 'status' and 'uptime' keys.
    """
    url = f"{base_url}/api/status"
    response = requests.get(url)

    # Assert status code is 200 OK
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Parse the JSON response
    response_data = response.json()

    # Assert that the response is a dictionary
    assert isinstance(response_data, dict)

    # Assert that the expected keys are in the response
    assert 'status' in response_data, "Response JSON is missing the 'status' key"
    assert 'uptime' in response_data, "Response JSON is missing the 'uptime' key"

    # Assert the status value
    assert response_data['status'] == 'online', f"Expected status to be 'online', but got '{response_data['status']}'"

# HEALING_TAG: GET_status
def test_get_status_negative_path_not_found(base_url):
    """
    Tests a negative path for the GET /api/status endpoint by using an incorrect path.
    Expects a 404 Not Found status.
    """
    url = f"{base_url}/api/nonexistent-status"
    response = requests.get(url)

    # Assert status code is 404 Not Found
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    
    # Assert that the response body contains an error key (framework dependent)
    # For many frameworks like Express, a default 404 might not have a JSON body
    # but a simple HTML or text response. We can check the content type.
    assert 'application/json' not in response.headers.get('Content-Type', ''), "Expected non-JSON response for 404"


# --- Tests for /api/update-profile Endpoint ---

# HEALING_TAG: POST_update-profile
def test_update_profile_happy_path(base_url):
    """
    Tests the happy path for the POST /api/update-profile endpoint.
    Sends a correctly structured payload and expects a 200 OK response.
    """
    url = f"{base_url}/api/update-profile"
    new_username = "qa_tester_001"
    payload = {
        "data": {
            "username": new_username
        }
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Assert status code is 200 OK
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Parse the JSON response
    response_data = response.json()

    # Assert that the response is a dictionary
    assert isinstance(response_data, dict)

    # Assert that the expected keys are in the response
    assert 'message' in response_data, "Response JSON is missing the 'message' key"
    assert 'success' in response_data, "Response JSON is missing the 'success' key"
    
    # Assert the content of the response
    assert response_data['message'] == f"Profile updated for {new_username}"
    assert response_data['success'] is True

# HEALING_TAG: POST_update-profile
def test_update_profile_negative_invalid_payload_structure(base_url):
    """
    Tests the negative path for the POST /api/update-profile endpoint.
    Sends a payload without the required nested 'data' object, which is known to cause a server crash.
    Expects a 500 Internal Server Error status.
    """
    url = f"{base_url}/api/update-profile"
    # This payload is intentionally incorrect; it's missing the 'data' wrapper.
    payload = {
        "username": "invalid_user"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Assert status code is 500 Internal Server Error
    assert response.status_code == 500, f"Expected status code 500, but got {response.status_code}"

    # A 500 error might not return a valid JSON. We can check for a generic error message in the text.
    # This assertion is flexible depending on the server's error verbosity.
    assert "Internal Server Error" in response.text or "Cannot read properties of undefined" in response.text, "Response body did not contain expected error message"