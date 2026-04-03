"""HTTP client for the DeviceBase API."""

from __future__ import annotations

import os
from typing import Any

import httpx

from devicebase.models import (
    AppInfo,
    Bounds,
    DeviceInfo,
    HierarchyInfo,
    InputTextRequest,
    LaunchAppRequest,
    OperationResult,
    Point,
)


class DeviceBaseError(Exception):
    """Base exception for DeviceBase SDK errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class DeviceNotFoundError(DeviceBaseError):
    """Raised when a device is not found or not connected."""

    pass


class ValidationError(DeviceBaseError):
    """Raised when request validation fails."""

    pass


class AuthenticationError(DeviceBaseError):
    """Raised when authentication fails."""

    pass


class DeviceBaseHttpClient:
    """HTTP client for interacting with the DeviceBase API.

    This client handles authentication, request/response serialization,
    and error handling for all HTTP-based API operations.

    Example:
        ```python
        client = DeviceBaseHttpClient(
            base_url="http://localhost:3410",
            api_key="your-jwt-token"
        )
        info = client.get_device_info("device123")
        ```
    """

    DEFAULT_BASE_URL = "https://api.devicebase.cn"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            base_url: The base URL of the DeviceBase API. If not provided,
                reads from DEVICEBASE_BASE_URL environment variable,
                defaults to https://api.devicebase.cn.
            api_key: JWT API key for authentication. If not provided,
                reads from DEVICEBASE_API_KEY environment variable.
            timeout: Request timeout in seconds.

        Raises:
            AuthenticationError: If no API key is provided via parameter
                or environment variable.
        """
        self._base_url = base_url or os.environ.get(
            "DEVICEBASE_BASE_URL", self.DEFAULT_BASE_URL
        )
        self._api_key = api_key or os.environ.get("DEVICEBASE_API_KEY")

        if not self._api_key:
            raise AuthenticationError(
                "API key is required. Provide it via 'api_key' parameter "
                "or DEVICEBASE_API_KEY environment variable."
            )

        self._timeout = timeout
        self._client = httpx.Client(
            base_url=self._base_url,
            headers=self._auth_headers(),
            timeout=timeout,
        )

    def _auth_headers(self) -> dict[str, str]:
        """Generate authentication headers with JWT token."""
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses."""
        if response.status_code == 404:
            raise DeviceNotFoundError(
                "Device not found or not connected", status_code=404
            )
        elif response.status_code == 422:
            raise ValidationError(
                f"Validation error: {response.text}", status_code=422
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed - invalid API key", status_code=401
            )
        elif response.status_code >= 400:
            raise DeviceBaseError(
                f"API error: {response.status_code} - {response.text}",
                status_code=response.status_code,
            )

    def _request(
        self,
        method: str,
        path: str,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request and handle the response."""
        response = self._client.request(method, path, json=json_data)
        self._handle_error(response)
        return response.json() if response.content else {}

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._client.close()

    def __enter__(self) -> DeviceBaseHttpClient:
        """Context manager entry."""
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.close()

    # Device Info API
    def get_device_info(self, serial: str) -> DeviceInfo:
        """Get detailed information about a device.

        Args:
            serial: The device unique identifier.

        Returns:
            DeviceInfo containing device status, hardware info, and connection state.

        Raises:
            DeviceNotFoundError: If the device is not found or not connected.
            ValidationError: If the serial is invalid.
        """
        data = self._request("POST", f"/v1/deviceinfo/{serial}")
        return DeviceInfo.from_dict(serial, data)

    # Device Control APIs
    def tap(self, serial: str, point: Point) -> OperationResult:
        """Perform a single tap at the specified coordinates.

        Args:
            serial: The device unique identifier.
            point: The coordinates where the tap should occur.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/tap/{serial}", point.to_dict())
        return OperationResult.from_dict(data)

    def double_tap(self, serial: str, point: Point) -> OperationResult:
        """Perform a double tap at the specified coordinates.

        Args:
            serial: The device unique identifier.
            point: The coordinates where the double tap should occur.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/double_tap/{serial}", point.to_dict())
        return OperationResult.from_dict(data)

    def long_press(self, serial: str, point: Point) -> OperationResult:
        """Perform a long press at the specified coordinates.

        Args:
            serial: The device unique identifier.
            point: The coordinates where the long press should occur.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/long_press/{serial}", point.to_dict())
        return OperationResult.from_dict(data)

    def swipe(self, serial: str, bounds: Bounds) -> OperationResult:
        """Perform a swipe gesture from start to end coordinates.

        Args:
            serial: The device unique identifier.
            bounds: The start (x1, y1) and end (x2, y2) coordinates.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/swipe/{serial}", bounds.to_dict())
        return OperationResult.from_dict(data)

    def back(self, serial: str) -> OperationResult:
        """Simulate the device back button press.

        Args:
            serial: The device unique identifier.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/back/{serial}")
        return OperationResult.from_dict(data)

    def home(self, serial: str) -> OperationResult:
        """Simulate the device home button press.

        Args:
            serial: The device unique identifier.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/home/{serial}")
        return OperationResult.from_dict(data)

    def launch_app(self, serial: str, app_name: str) -> OperationResult:
        """Launch an application on the device.

        Args:
            serial: The device unique identifier.
            app_name: The package name or identifier of the app to launch.

        Returns:
            OperationResult indicating success or failure.
        """
        request = LaunchAppRequest(app_name=app_name)
        data = self._request("POST", f"/v1/launch_app/{serial}", request.to_dict())
        return OperationResult.from_dict(data)

    def input_text(self, serial: str, text: str) -> OperationResult:
        """Input text into the currently focused field.

        Args:
            serial: The device unique identifier.
            text: The text to input.

        Returns:
            OperationResult indicating success or failure.
        """
        request = InputTextRequest(text=text)
        data = self._request("POST", f"/v1/input/{serial}", request.to_dict())
        return OperationResult.from_dict(data)

    def clear_text(self, serial: str) -> OperationResult:
        """Clear text in the currently focused field.

        Args:
            serial: The device unique identifier.

        Returns:
            OperationResult indicating success or failure.
        """
        data = self._request("POST", f"/v1/clear_text/{serial}")
        return OperationResult.from_dict(data)

    def get_current_app(self, serial: str) -> AppInfo:
        """Get information about the currently running foreground app.

        Args:
            serial: The device unique identifier.

        Returns:
            AppInfo containing the current app name and details.
        """
        data = self._request("POST", f"/v1/current_app/{serial}")
        return AppInfo.from_dict(data)

    def dump_hierarchy(self, serial: str) -> HierarchyInfo:
        """Get the current UI hierarchy structure.

        Args:
            serial: The device unique identifier.

        Returns:
            HierarchyInfo containing the UI element tree.
        """
        data = self._request("POST", f"/v1/dump_hierarchy/{serial}")
        return HierarchyInfo.from_dict(data)

    # Screenshot APIs
    def get_screenshot(self, serial: str) -> bytes:
        """Get a screenshot of the device screen as JPEG bytes.

        Args:
            serial: The device unique identifier.

        Returns:
            Raw JPEG image bytes.

        Raises:
            DeviceNotFoundError: If the device is not found.
        """
        response = self._client.get(f"/v1/screen/{serial}")
        self._handle_error(response)
        return response.content

    def get_screenshot_post(self, serial: str) -> bytes:
        """Get a screenshot using POST method (alternative to GET).

        Args:
            serial: The device unique identifier.

        Returns:
            Raw JPEG image bytes.
        """
        response = self._client.post(f"/v1/screen/{serial}")
        self._handle_error(response)
        return response.content

    def download_screenshot(self, serial: str) -> bytes:
        """Download screenshot as a file attachment.

        Args:
            serial: The device unique identifier.

        Returns:
            Raw JPEG image bytes with filename {serial}_screenshot.jpg.
        """
        response = self._client.get(f"/v1/screenshot/{serial}")
        self._handle_error(response)
        return response.content

    # MJPEG Stream
    def get_mjpeg_stream(self, serial: str) -> httpx.Response:
        """Get the MJPEG video stream response.

        This returns a raw response that can be iterated for frames.
        For a higher-level interface, use the WebSocket clients.

        Args:
            serial: The device unique identifier.

        Returns:
            Raw HTTP response for streaming.
        """
        response = self._client.get(
            f"/v1/mjpeg/{serial}",
            headers={**self._auth_headers(), "Accept": "multipart/x-mixed-replace"},
        )
        self._handle_error(response)
        return response
