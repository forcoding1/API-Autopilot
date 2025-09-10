
import requests
from typing import Dict, Any, Optional

class TimerAPIError(Exception):
    """Custom exception for TimerAPI errors."""
    pass

class TimerAPI:
    """
    Python client for interacting with the Timer API.

    This client provides methods to create, start, and resume timers.
    It handles API key authentication and basic error handling.
    """

    # Base URL for the Timer API.
    # NOTE: The base_url was not provided in the structured metadata.
    # Please replace this with the actual base URL of your API.
    BASE_URL = "https://api.example.com"

    def __init__(self, api_key: str):
        """
        Initializes the TimerAPI client.

        Args:
            api_key: Your API key for authentication.
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        """
        Returns the common headers for API requests, including authentication.

        NOTE: Assuming API key is passed via 'X-API-Key' header.
        Adjust header name if your API uses a different one (e.g., 'Authorization: Bearer YOUR_KEY').
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-Key": self.api_key,
        }

    def _request(self, method: str, path: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Internal helper for making HTTP requests to the API.

        Args:
            method: The HTTP method (e.g., 'GET', 'POST', 'PUT').
            path: The API endpoint path (e.g., '/timer/').
            json_data: Optional dictionary to be sent as JSON body.

        Returns:
            A dictionary representing the JSON response from the API.

        Raises:
            TimerAPIError: For network errors or unsuccessful API responses.
        """
        url = f"{self.BASE_URL}{path}"
        headers = self._get_headers()

        try:
            response = requests.request(method, url, headers=headers, json=json_data, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.Timeout:
            raise TimerAPIError(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError as e:
            raise TimerAPIError(f"Failed to connect to {url}: {e}")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_message = e.response.text
            raise TimerAPIError(f"API request failed with status {status_code}: {error_message}")
        except requests.exceptions.RequestException as e:
            raise TimerAPIError(f"An unexpected request error occurred: {e}")
        except ValueError: # JSONDecodeError is a subclass of ValueError
            # This handles cases where the response is not valid JSON, but the status code was 2xx
            raise TimerAPIError(f"Received non-JSON response from {url}: {response.text}")

    def create_and_start_timer(
        self,
        person_id: int,
        task_id: Optional[int] = None,
        starttime: Optional[str] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates and immediately starts a new timer.

        If 'starttime' is provided, it uses that time; otherwise, it uses server time.

        Args:
            person_id: The ID of the person this timer is associated with. (Required)
            task_id: The ID of the task this timer is associated with. If left blank,
                     this timer will be a General Timer. (Optional)
            starttime: The UTC time when the timer started, in ISO 8601 format (e.g., "2024-07-18T10:30:00Z").
                       If omitted, server time will be used. (Optional)
            name: A description for the timer (max 255 characters). (Optional)

        Returns:
            A dictionary representing the newly created timer object.

        Raises:
            ValueError: If `person_id` is missing.
            TimerAPIError: For network or API-specific errors.
        """
        if not isinstance(person_id, int):
            raise ValueError("person_id must be an integer.")

        payload: Dict[str, Any] = {"personid": person_id}
        if task_id is not None:
            payload["taskid"] = task_id
        if starttime is not None:
            payload["starttime"] = starttime
        if name is not None:
            payload["name"] = name

        return self._request(method='POST', path='/timer/', json_data=payload)

    def resume_timer(
        self,
        timer_id: int,
        starttime: str,
        task_id: Optional[int] = None,
        person_id: Optional[int] = None,
        name: Optional[str] = None,
        lastupdate: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resumes a paused timer by setting its 'starttime' to the current UTC time.

        Args:
            timer_id: The ID of the timer to resume. (Required)
            starttime: The current UTC time to set as the timer's start time,
                       effectively resuming it, in ISO 8601 format (e.g., "2024-07-18T10:35:00Z"). (Required)
            task_id: The ID of the task this timer is associated with. (Optional)
            person_id: The ID of the person this timer is associated with. (Optional)
            name: A description for the timer (max 255 characters). (Optional)
            lastupdate: The date on which the timer was last started or stopped, in ISO 8601 format. (Optional)

        Returns:
            A dictionary representing the updated timer object.

        Raises:
            ValueError: If `timer_id` or `starttime` is missing or invalid.
            TimerAPIError: For network or API-specific errors.
        """
        if not isinstance(timer_id, int):
            raise ValueError("timer_id must be an integer.")
        if not isinstance(starttime, str) or not starttime:
            raise ValueError("starttime must be a non-empty string in ISO 8601 format.")

        payload: Dict[str, Any] = {"starttime": starttime}
        if task_id is not None:
            payload["taskid"] = task_id
        if person_id is not None:
            payload["personid"] = person_id
        if name is not None:
            payload["name"] = name
        if lastupdate is not None:
            payload["lastupdate"] = lastupdate

        return self._request(method='PUT', path=f'/timer/{timer_id}/', json_data=payload)

if __name__ == "__main__":
    # --- Configuration ---
    # Replace with your actual API key
    # For security, consider loading this from environment variables or a configuration file.
    YOUR_API_KEY = "YOUR_SECRET_API_KEY"

    # --- Client Initialization ---
    try:
        client = TimerAPI(api_key=YOUR_API_KEY)
        print("TimerAPI client initialized successfully.")
    except ValueError as e:
        print(f"Error initializing TimerAPI client: {e}")
        exit(1)

    # --- Example Usage: Create and Start a Timer ---
    print("\n--- Creating and Starting a New Timer ---")
    try:
        new_timer_data = client.create_and_start_timer(
            person_id=123,
            starttime="2024-07-18T10:30:00Z",
            name="Working on feature X",
            task_id=456
        )
        print("Successfully created and started timer:")
        print(new_timer_data)
        # Assuming the response includes an 'id' for the created timer
        created_timer_id = new_timer_data.get("id")
        if created_timer_id:
            print(f"Created Timer ID: {created_timer_id}")
        else:
            print("Warning: 'id' not found in the new timer response.")

    except TimerAPIError as e:
        print(f"Error creating timer: {e}")
    except ValueError as e:
        print(f"Validation error for creating timer: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during timer creation: {e}")


    # --- Example Usage: Resume a Timer ---
    print("\n--- Resuming an Existing Timer ---")
    # Use a placeholder ID or the ID from the previously created timer if available
    timer_to_resume_id = created_timer_id if 'created_timer_id' in locals() and created_timer_id else 789

    try:
        resumed_timer_data = client.resume_timer(
            timer_id=timer_to_resume_id,
            starttime="2024-07-18T10:35:00Z",
            name="Resumed work on feature X",
            lastupdate="2024-07-17T15:00:00Z"
        )
        print(f"Successfully resumed timer (ID: {timer_to_resume_id}):")
        print(resumed_timer_data)
    except TimerAPIError as e:
        print(f"Error resuming timer (ID: {timer_to_resume_id}): {e}")
    except ValueError as e:
        print(f"Validation error for resuming timer: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during timer resumption: {e}")

    # --- Example Usage: Error Case (Missing Required Parameter) ---
    print("\n--- Example Error Case: Missing person_id for create_and_start_timer ---")
    try:
        # Intentionally omitting person_id
        client.create_and_start_timer(person_id=None, name="Invalid call") # type: ignore
    except ValueError as e:
        print(f"Caught expected validation error: {e}")
    except TimerAPIError as e:
        print(f"Caught API error: {e}")
    except Exception as e:
        print(f"Caught unexpected error: {e}")

    # --- Example Usage: Error Case (Invalid timer_id type for resume_timer) ---
    print("\n--- Example Error Case: Invalid timer_id type for resume_timer ---")
    try:
        # Intentionally passing wrong type for timer_id
        client.resume_timer(timer_id="invalid_id", starttime="2024-07-18T11:00:00Z") # type: ignore
    except ValueError as e:
        print(f"Caught expected validation error: {e}")
    except TimerAPIError as e:
        print(f"Caught API error: {e}")
    except Exception as e:
        print(f"Caught unexpected error: {e}")