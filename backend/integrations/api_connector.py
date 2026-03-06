import requests
from backend.utils.logger import log_info, log_error
from backend.services.api_key_manager import get_api_key


class APIConnector:
    """API connector class for making HTTP requests with API key support"""

    @staticmethod
    def get(url: str, headers=None, params=None, api_key_name=None):
        """
        Make a GET request

        Args:
            url: Target URL
            headers: Request headers
            params: Query parameters
            api_key_name: Name of API key to include in headers

        Returns:
            Response dictionary
        """
        try:
            if api_key_name:
                api_key = get_api_key(api_key_name)
                if api_key:
                    headers = headers or {}
                    headers["Authorization"] = f"Bearer {api_key}"

            response = requests.get(url, headers=headers, params=params, timeout=10)
            return {
                "status": response.status_code,
                "data": response.json() if response.text else {}
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def post(url: str, headers=None, data=None, api_key_name=None):
        """
        Make a POST request

        Args:
            url: Target URL
            headers: Request headers
            data: Request body (JSON)
            api_key_name: Name of API key to include in headers

        Returns:
            Response dictionary
        """
        try:
            if api_key_name:
                api_key = get_api_key(api_key_name)
                if api_key:
                    headers = headers or {}
                    headers["Authorization"] = f"Bearer {api_key}"

            response = requests.post(url, headers=headers, json=data, timeout=10)
            return {
                "status": response.status_code,
                "data": response.json() if response.text else {}
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def put(url: str, headers=None, data=None, api_key_name=None):
        """
        Make a PUT request

        Args:
            url: Target URL
            headers: Request headers
            data: Request body (JSON)
            api_key_name: Name of API key to include in headers

        Returns:
            Response dictionary
        """
        try:
            if api_key_name:
                api_key = get_api_key(api_key_name)
                if api_key:
                    headers = headers or {}
                    headers["Authorization"] = f"Bearer {api_key}"

            response = requests.put(url, headers=headers, json=data, timeout=10)
            return {
                "status": response.status_code,
                "data": response.json() if response.text else {}
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def delete(url: str, headers=None, params=None, api_key_name=None):
        """
        Make a DELETE request

        Args:
            url: Target URL
            headers: Request headers
            params: Query parameters
            api_key_name: Name of API key to include in headers

        Returns:
            Response dictionary
        """
        try:
            if api_key_name:
                api_key = get_api_key(api_key_name)
                if api_key:
                    headers = headers or {}
                    headers["Authorization"] = f"Bearer {api_key}"

            response = requests.delete(url, headers=headers, params=params, timeout=10)
            return {
                "status": response.status_code,
                "data": response.json() if response.text else {}
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


def call_api_action(url: str, method: str = "POST", payload: dict = None, headers: dict = None, api_key_name: str = None):
    """
    Wrapper function to call an API with optional API key authentication

    Args:
        url: API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE)
        payload: Request body
        headers: Request headers
        api_key_name: Name of stored API key to use for authentication

    Returns:
        API response
    """
    try:
        if not url:
            return {
                "status": "error",
                "message": "URL not provided"
            }

        method = method.upper() if method else "POST"

        log_info(f"Calling API: {method} {url}")

        if method == "GET":
            result = APIConnector.get(url, headers=headers, params=payload, api_key_name=api_key_name)
        elif method == "POST":
            result = APIConnector.post(url, headers=headers, data=payload, api_key_name=api_key_name)
        elif method == "PUT":
            result = APIConnector.put(url, headers=headers, data=payload, api_key_name=api_key_name)
        elif method == "DELETE":
            result = APIConnector.delete(url, headers=headers, params=payload, api_key_name=api_key_name)
        else:
            result = {
                "status": "error",
                "message": f"Unsupported HTTP method: {method}"
            }

        log_info(f"API call result: {result}")
        return result

    except Exception as e:
        log_error(f"Error calling API: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def configure_api_integration(api_name: str, api_key: str, base_url: str = None):
    """
    Configure API integration with API keys

    Args:
        api_name: Name identifier for the API (e.g., "openai", "slack")
        api_key: API key value
        base_url: Base URL for the API (optional)
    """
    from backend.services.api_key_manager import set_api_key

    set_api_key(f"{api_name}_api_key", api_key)
    if base_url:
        set_api_key(f"{api_name}_base_url", base_url)

    log_info(f"API integration configured for {api_name}")


def test_api_integration(api_name: str, test_url: str = None):
    """
    Test API integration by making a test call

    Args:
        api_name: Name of the configured API
        test_url: Test endpoint URL (optional, will use base_url + /test if not provided)

    Returns:
        Test result
    """
    base_url = get_api_key(f"{api_name}_base_url")
    api_key_name = f"{api_name}_api_key"

    if not base_url and not test_url:
        return {
            "status": "error",
            "message": f"No base URL configured for {api_name}"
        }

    url = test_url or f"{base_url}/test"

    return call_api_action(
        url=url,
        method="GET",
        api_key_name=api_key_name
    )