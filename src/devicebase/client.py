"""Main DeviceBase client providing high-level access to all device operations."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

from devicebase.http_client import (
    AuthenticationError,
    DeviceBaseHttpClient,
)
from devicebase.models import (
    AppInfo,
    Bounds,
    DeviceInfo,
    HierarchyInfo,
    OperationResult,
    Point,
)
from devicebase.websocket_client import MinicapClient, MinitouchClient


class DeviceBaseClient:
    """Main client for interacting with the DeviceBase API.

    This client provides a unified interface for all device automation operations,
    including HTTP-based device control and WebSocket-based streaming and touch control.

    Configuration can be provided via constructor parameters or environment variables:
    - DEVICEBASE_BASE_URL: API base URL (default: https://api.devicebase.cn)
    - DEVICEBASE_API_KEY: JWT API key for authentication

    Example:
        ```python
        import asyncio
        from devicebase import DeviceBaseClient

        # Using environment variables
        client = DeviceBaseClient()

        # Or with explicit configuration
        client = DeviceBaseClient(
            base_url="https://api.devicebase.cn",
            api_key="your-jwt-token"
        )

        # Get device info
        info = client.get_device_info("device123")

        # Control the device
        client.tap("device123", Point(x=100, y=200))
        client.launch_app("device123", "com.example.app")

        # WebSocket streaming (async)
        async def stream_screen():
            async for frame in client.stream_minicap("device123"):
                # Process JPEG frame
                pass

        asyncio.run(stream_screen())
        ```
    """

    DEFAULT_BASE_URL = "https://api.devicebase.cn"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the DeviceBase client.

        Args:
            base_url: The base URL of the DeviceBase API. If not provided,
                reads from DEVICEBASE_BASE_URL environment variable,
                defaults to https://api.devicebase.cn.
            api_key: JWT API key for authentication. If not provided,
                reads from DEVICEBASE_API_KEY environment variable.
            timeout: Request timeout in seconds for HTTP operations.

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

        self._http = DeviceBaseHttpClient(
            base_url=self._base_url,
            api_key=self._api_key,
            timeout=timeout,
        )

    def close(self) -> None:
        """Close the client and release all resources."""
        self._http.close()

    def __enter__(self) -> DeviceBaseClient:
        """Context manager entry."""
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.close()

    # Device Info
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
        return self._http.get_device_info(serial)

    # Touch Operations
    def tap(self, serial: str, x: int, y: int) -> OperationResult:
        """Perform a single tap at the specified coordinates.

        Args:
            serial: The device unique identifier.
            x: Horizontal coordinate (pixels from left).
            y: Vertical coordinate (pixels from top).

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.tap(serial, Point(x=x, y=y))

    def double_tap(self, serial: str, x: int, y: int) -> OperationResult:
        """Perform a double tap at the specified coordinates.

        Args:
            serial: The device unique identifier.
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.double_tap(serial, Point(x=x, y=y))

    def long_press(self, serial: str, x: int, y: int) -> OperationResult:
        """Perform a long press at the specified coordinates.

        Args:
            serial: The device unique identifier.
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.long_press(serial, Point(x=x, y=y))

    def swipe(
        self, serial: str, x1: int, y1: int, x2: int, y2: int
    ) -> OperationResult:
        """Perform a swipe gesture from start to end coordinates.

        Args:
            serial: The device unique identifier.
            x1: Starting X coordinate.
            y1: Starting Y coordinate.
            x2: Ending X coordinate.
            y2: Ending Y coordinate.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.swipe(serial, Bounds(x1=x1, y1=y1, x2=x2, y2=y2))

    # Navigation
    def back(self, serial: str) -> OperationResult:
        """Simulate the device back button press.

        Args:
            serial: The device unique identifier.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.back(serial)

    def home(self, serial: str) -> OperationResult:
        """Simulate the device home button press.

        Args:
            serial: The device unique identifier.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.home(serial)

    # App Operations
    def launch_app(self, serial: str, app_name: str) -> OperationResult:
        """Launch an application on the device.

        Args:
            serial: The device unique identifier.
            app_name: The package name or identifier of the app to launch.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.launch_app(serial, app_name)

    def get_current_app(self, serial: str) -> AppInfo:
        """Get information about the currently running foreground app.

        Args:
            serial: The device unique identifier.

        Returns:
            AppInfo containing the current app name and details.
        """
        return self._http.get_current_app(serial)

    # Text Input
    def input_text(self, serial: str, text: str) -> OperationResult:
        """Input text into the currently focused field.

        Args:
            serial: The device unique identifier.
            text: The text to input.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.input_text(serial, text)

    def clear_text(self, serial: str) -> OperationResult:
        """Clear text in the currently focused field.

        Args:
            serial: The device unique identifier.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.clear_text(serial)

    # UI Hierarchy
    def dump_hierarchy(self, serial: str) -> HierarchyInfo:
        """Get the current UI hierarchy structure.

        Args:
            serial: The device unique identifier.

        Returns:
            HierarchyInfo containing the UI element tree.
        """
        return self._http.dump_hierarchy(serial)

    # Screenshots
    def get_screenshot(self, serial: str) -> bytes:
        """Get a screenshot of the device screen as JPEG bytes.

        Args:
            serial: The device unique identifier.

        Returns:
            Raw JPEG image bytes.

        Raises:
            DeviceNotFoundError: If the device is not found.
        """
        return self._http.get_screenshot(serial)

    def download_screenshot(self, serial: str) -> bytes:
        """Download screenshot as a file attachment.

        The filename will be {serial}_screenshot.jpg.

        Args:
            serial: The device unique identifier.

        Returns:
            Raw JPEG image bytes.
        """
        return self._http.download_screenshot(serial)

    # WebSocket Clients
    def minicap_client(self, serial: str) -> MinicapClient:
        """Create a minicap WebSocket client for screen streaming.

        Args:
            serial: The device unique identifier.

        Returns:
            MinicapClient configured for the device.

        Example:
            ```python
            client = DeviceBaseClient()
            minicap = client.minicap_client("device123")

            async for frame in minicap.stream_frames():
                # Process JPEG frame
                pass
            ```
        """
        return MinicapClient(
            base_url=self._base_url,
            serial=serial,
            api_key=self._api_key,
        )

    def minitouch_client(self, serial: str) -> MinitouchClient:
        """Create a minitouch WebSocket client for touch control.

        Args:
            serial: The device unique identifier.

        Returns:
            MinitouchClient configured for the device.

        Example:
            ```python
            client = DeviceBaseClient()
            minitouch = client.minitouch_client("device123")

            async with minitouch:
                await minitouch.tap(100, 200)
            ```
        """
        return MinitouchClient(
            base_url=self._base_url,
            serial=serial,
            api_key=self._api_key,
        )

    # Async streaming convenience methods
    def stream_minicap(self, serial: str) -> AsyncIterator[bytes]:
        """Stream JPEG frames from the device screen.

        This is a convenience method that creates a minicap client
        and yields frames from its stream.

        Args:
            serial: The device unique identifier.

        Yields:
            JPEG image bytes for each frame.

        Example:
            ```python
            client = DeviceBaseClient()

            async for frame in client.stream_minicap("device123"):
                with open("frame.jpg", "wb") as f:
                    f.write(frame)
            ```
        """
        client = self.minicap_client(serial)
        return client.stream_frames()
