"""Tests for DeviceBase main client."""

import os
from unittest.mock import MagicMock, patch

import pytest

from devicebase import (
    AuthenticationError,
    DeviceBaseClient,
)
from devicebase.models import Bounds, Point


class TestDeviceBaseClientInit:
    """Tests for main client initialization."""

    def test_init_with_explicit_params(self) -> None:
        client = DeviceBaseClient(
            serial="device123",
            base_url="http://test.com",
            api_key="test-key",
        )
        assert client._serial == "device123"
        assert client._base_url == "http://test.com"
        assert client._api_key == "test-key"
        client.close()

    def test_init_with_env_vars(self) -> None:
        with patch.dict(
            os.environ,
            {"DEVICEBASE_BASE_URL": "http://env.com", "DEVICEBASE_API_KEY": "env-key"},
        ):
            client = DeviceBaseClient(serial="device123")
            assert client._base_url == "http://env.com"
            assert client._api_key == "env-key"
            client.close()

    def test_init_missing_api_key_raises(self) -> None:
        with patch.dict(os.environ, {}, clear=True), pytest.raises(AuthenticationError):
            DeviceBaseClient(serial="device123")


class TestDeviceBaseClientContextManager:
    """Tests for context manager usage."""

    def test_context_manager(self) -> None:
        with (
            patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}),
            DeviceBaseClient(serial="device123") as client,
        ):
            assert isinstance(client, DeviceBaseClient)


class TestDeviceBaseClientTouchOperations:
    """Tests for touch operations."""

    def test_tap(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.tap.return_value = MagicMock(success=True)

            result = client.tap(x=100, y=200)

            assert result.success is True
            client._http.tap.assert_called_once_with("device123", Point(x=100, y=200))
            client.close()

    def test_double_tap(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.double_tap.return_value = MagicMock(success=True)

            result = client.double_tap(x=50, y=75)

            assert result.success is True
            client._http.double_tap.assert_called_once_with("device123", Point(x=50, y=75))
            client.close()

    def test_long_press(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.long_press.return_value = MagicMock(success=True)

            result = client.long_press(x=100, y=200)

            assert result.success is True
            client._http.long_press.assert_called_once_with("device123", Point(x=100, y=200))
            client.close()

    def test_swipe(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.swipe.return_value = MagicMock(success=True)

            result = client.swipe(x1=0, y1=0, x2=100, y2=200)

            assert result.success is True
            client._http.swipe.assert_called_once_with(
                "device123", Bounds(x1=0, y1=0, x2=100, y2=200)
            )
            client.close()


class TestDeviceBaseClientNavigation:
    """Tests for navigation operations."""

    def test_back(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.back.return_value = MagicMock(success=True)

            result = client.back()

            assert result.success is True
            client._http.back.assert_called_once_with("device123")
            client.close()

    def test_home(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.home.return_value = MagicMock(success=True)

            result = client.home()

            assert result.success is True
            client._http.home.assert_called_once_with("device123")
            client.close()


class TestDeviceBaseClientAppOperations:
    """Tests for app operations."""

    def test_launch_app(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.launch_app.return_value = MagicMock(success=True)

            result = client.launch_app("com.example.app")

            assert result.success is True
            client._http.launch_app.assert_called_once_with("device123", "com.example.app")
            client.close()

    def test_get_current_app(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            mock_app_info = MagicMock()
            mock_app_info.data = {"package": "com.example.app"}
            client._http.get_current_app.return_value = mock_app_info

            result = client.get_current_app()

            assert result.data["package"] == "com.example.app"
            client._http.get_current_app.assert_called_once_with("device123")
            client.close()


class TestDeviceBaseClientTextInput:
    """Tests for text input operations."""

    def test_input_text(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.input_text.return_value = MagicMock(success=True)

            result = client.input_text("Hello World")

            assert result.success is True
            client._http.input_text.assert_called_once_with("device123", "Hello World")
            client.close()

    def test_clear_text(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            client._http = MagicMock()
            client._http.clear_text.return_value = MagicMock(success=True)

            result = client.clear_text()

            assert result.success is True
            client._http.clear_text.assert_called_once_with("device123")
            client.close()


class TestDeviceBaseClientWebSocketClients:
    """Tests for WebSocket client factory methods."""

    def test_minicap_client(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            minicap = client.minicap_client()

            assert minicap._serial == "device123"
            assert minicap._api_key == "test-key"
            client.close()

    def test_minitouch_client(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseClient(serial="device123")
            minitouch = client.minitouch_client()

            assert minitouch._serial == "device123"
            assert minitouch._api_key == "test-key"
            client.close()
