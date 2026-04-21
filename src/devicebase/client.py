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
        client = DeviceBaseClient(serial="device123")

        # Or with explicit configuration
        client = DeviceBaseClient(
            serial="device123",
            base_url="https://api.devicebase.cn",
            api_key="your-jwt-token"
        )

        # Get device info
        info = client.get_device_info()

        # Control the device
        client.tap(Point(x=100, y=200))
        client.launch_app("com.example.app")

        # WebSocket streaming (async)
        async def stream_screen():
            async for frame in client.stream_minicap():
                # Process JPEG frame
                pass

        asyncio.run(stream_screen())
        ```
    """

    DEFAULT_BASE_URL = "https://api.devicebase.cn"

    def __init__(
        self,
        serial: str,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the DeviceBase client.

        Args:
            serial: The device unique identifier.
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
        self._serial = serial
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
    def get_device_info(self) -> DeviceInfo:
        """Get detailed information about the device.

        Returns:
            DeviceInfo containing device status, hardware info, and connection state.

        Raises:
            DeviceNotFoundError: If the device is not found or not connected.
            ValidationError: If the serial is invalid.
        """
        return self._http.get_device_info(self._serial)

    # Touch Operations
    def tap(self, x: int, y: int) -> OperationResult:
        """Perform a single tap at the specified coordinates.

        Args:
            x: Horizontal coordinate (pixels from left).
            y: Vertical coordinate (pixels from top).

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.tap(self._serial, Point(x=x, y=y))

    def double_tap(self, x: int, y: int) -> OperationResult:
        """Perform a double tap at the specified coordinates.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.double_tap(self._serial, Point(x=x, y=y))

    def long_press(self, x: int, y: int) -> OperationResult:
        """Perform a long press at the specified coordinates.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.long_press(self._serial, Point(x=x, y=y))

    def swipe(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> OperationResult:
        """Perform a swipe gesture from start to end coordinates.

        Args:
            x1: Starting X coordinate.
            y1: Starting Y coordinate.
            x2: Ending X coordinate.
            y2: Ending Y coordinate.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.swipe(self._serial, Bounds(x1=x1, y1=y1, x2=x2, y2=y2))

    # Navigation
    def back(self) -> OperationResult:
        """Simulate the device back button press.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.back(self._serial)

    def home(self) -> OperationResult:
        """Simulate the device home button press.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.home(self._serial)

    # App Operations
    def launch_app(self, app_name: str) -> OperationResult:
        """Launch an application on the device.

        Args:
            app_name: The package name or identifier of the app to launch.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.launch_app(self._serial, app_name)

    def get_current_app(self) -> AppInfo:
        """Get information about the currently running foreground app.

        Returns:
            AppInfo containing the current app name and details.
        """
        return self._http.get_current_app(self._serial)

    # Text Input
    def input_text(self, text: str) -> OperationResult:
        """Input text into the currently focused field.

        Args:
            text: The text to input.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.input_text(self._serial, text)

    def clear_text(self) -> OperationResult:
        """Clear text in the currently focused field.

        Returns:
            OperationResult indicating success or failure.
        """
        return self._http.clear_text(self._serial)

    # UI Hierarchy
    def dump_hierarchy(self) -> HierarchyInfo:
        """Get the current UI hierarchy structure.

        Returns:
            HierarchyInfo containing the UI element tree.
        """
        return self._http.dump_hierarchy(self._serial)

    # Screenshots
    def get_screenshot(self) -> bytes:
        """Get a screenshot of the device screen as JPEG bytes.

        Returns:
            Raw JPEG image bytes.

        Raises:
            DeviceNotFoundError: If the device is not found.
        """
        return self._http.get_screenshot(self._serial)

    def download_screenshot(self) -> bytes:
        """Download screenshot as a file attachment.

        The filename will be {serial}_screenshot.jpg.

        Returns:
            Raw JPEG image bytes.
        """
        return self._http.download_screenshot(self._serial)

    # WebSocket Clients
    def minicap_client(self) -> MinicapClient:
        """Create a minicap WebSocket client for screen streaming.

        Returns:
            MinicapClient configured for the device.

        Example:
            ```python
            client = DeviceBaseClient(serial="device123")
            minicap = client.minicap_client()

            async for frame in minicap.stream_frames():
                # Process JPEG frame
                pass
            ```
        """
        return MinicapClient(
            base_url=self._base_url,
            serial=self._serial,
            api_key=self._api_key,
        )

    def minitouch_client(self) -> MinitouchClient:
        """Create a minitouch WebSocket client for touch control.

        Returns:
            MinitouchClient configured for the device.

        Example:
            ```python
            client = DeviceBaseClient(serial="device123")
            minitouch = client.minitouch_client()

            async with minitouch:
                await minitouch.tap(100, 200)
            ```
        """
        return MinitouchClient(
            base_url=self._base_url,
            serial=self._serial,
            api_key=self._api_key,
        )

    # Async streaming convenience methods
    def stream_minicap(self) -> AsyncIterator[bytes]:
        """Stream JPEG frames from the device screen.

        This is a convenience method that creates a minicap client
        and yields frames from its stream.

        Yields:
            JPEG image bytes for each frame.

        Example:
            ```python
            client = DeviceBaseClient(serial="device123")

            async for frame in client.stream_minicap():
                with open("frame.jpg", "wb") as f:
                    f.write(frame)
            ```
        """
        client = self.minicap_client()
        return client.stream_frames()
