"""Tests for DeviceBase HTTP client."""

import os
from unittest.mock import patch

import httpx
import pytest
import respx

from devicebase.http_client import (
    AuthenticationError,
    DeviceBaseError,
    DeviceBaseHttpClient,
    DeviceNotFoundError,
    ValidationError,
)
from devicebase.models import Bounds, Point


class TestDeviceBaseHttpClientInit:
    """Tests for HTTP client initialization."""

    def test_init_with_explicit_params(self) -> None:
        client = DeviceBaseHttpClient(
            base_url="http://test.com",
            api_key="test-key",
        )
        assert client._base_url == "http://test.com"
        assert client._api_key == "test-key"
        client.close()

    def test_init_with_env_vars(self) -> None:
        with patch.dict(
            os.environ,
            {"DEVICEBASE_BASE_URL": "http://env.com", "DEVICEBASE_API_KEY": "env-key"},
        ):
            client = DeviceBaseHttpClient()
            assert client._base_url == "http://env.com"
            assert client._api_key == "env-key"
            client.close()

    def test_init_default_base_url(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "test-key"}):
            client = DeviceBaseHttpClient()
            assert client._base_url == "https://api.devicebase.cn"
            client.close()

    def test_init_missing_api_key_raises(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(AuthenticationError) as exc_info:
                DeviceBaseHttpClient()
            assert "API key is required" in str(exc_info.value)


class TestDeviceBaseHttpClientErrors:
    """Tests for HTTP client error handling."""

    @respx.mock
    def test_device_not_found_error(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/deviceinfo/device123").mock(
            return_value=httpx.Response(404)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            with pytest.raises(DeviceNotFoundError) as exc_info:
                client.get_device_info("device123")
            assert exc_info.value.status_code == 404

    @respx.mock
    def test_validation_error(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/tap/device123").mock(
            return_value=httpx.Response(422, json={"detail": "Invalid coordinates"})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            with pytest.raises(ValidationError) as exc_info:
                client.tap("device123", Point(x=100, y=200))
            assert exc_info.value.status_code == 422

    @respx.mock
    def test_generic_api_error(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/deviceinfo/device123").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            with pytest.raises(DeviceBaseError) as exc_info:
                client.get_device_info("device123")
            assert exc_info.value.status_code == 500


class TestDeviceInfoAPI:
    """Tests for device info API."""

    @respx.mock
    def test_get_device_info_success(self) -> None:
        response_data = {
            "status": "online",
            "battery": 85,
            "screen": {"width": 1080, "height": 1920},
        }
        _ = respx.post("https://api.devicebase.cn/v1/deviceinfo/device123").mock(
            return_value=httpx.Response(200, json=response_data)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            info = client.get_device_info("device123")

        assert info.serial == "device123"
        assert info.data == response_data


class TestDeviceControlAPIs:
    """Tests for device control APIs."""

    @respx.mock
    def test_tap(self) -> None:
        route = respx.post("https://api.devicebase.cn/v1/tap/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.tap("device123", Point(x=100, y=200))

        assert result.success is True
        assert route.called
        request_body = route.calls.last.request.content
        assert b'"x"' in request_body
        assert b'"y"' in request_body

    @respx.mock
    def test_double_tap(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/double_tap/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.double_tap("device123", Point(x=50, y=75))

        assert result.success is True

    @respx.mock
    def test_long_press(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/long_press/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.long_press("device123", Point(x=100, y=200))

        assert result.success is True

    @respx.mock
    def test_swipe(self) -> None:
        route = respx.post("https://api.devicebase.cn/v1/swipe/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.swipe("device123", Bounds(x1=0, y1=0, x2=100, y2=200))

        assert result.success is True
        assert route.called
        request_body = route.calls.last.request.content
        assert b'"x1"' in request_body
        assert b'"y2"' in request_body

    @respx.mock
    def test_back(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/back/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.back("device123")

        assert result.success is True

    @respx.mock
    def test_home(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/home/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.home("device123")

        assert result.success is True


class TestAppOperations:
    """Tests for app-related operations."""

    @respx.mock
    def test_launch_app(self) -> None:
        route = respx.post("https://api.devicebase.cn/v1/launch_app/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.launch_app("device123", "com.example.app")

        assert result.success is True
        assert route.called
        request_body = route.calls.last.request.content
        assert b'"app_name"' in request_body

    @respx.mock
    def test_get_current_app(self) -> None:
        response_data = {"package": "com.example.app", "activity": ".MainActivity"}
        _ = respx.post("https://api.devicebase.cn/v1/current_app/device123").mock(
            return_value=httpx.Response(200, json=response_data)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            info = client.get_current_app("device123")

        assert info.data == response_data


class TestTextInput:
    """Tests for text input operations."""

    @respx.mock
    def test_input_text(self) -> None:
        route = respx.post("https://api.devicebase.cn/v1/input/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.input_text("device123", "Hello World")

        assert result.success is True
        assert route.called
        request_body = route.calls.last.request.content
        assert b'"text"' in request_body

    @respx.mock
    def test_clear_text(self) -> None:
        _ = respx.post("https://api.devicebase.cn/v1/clear_text/device123").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.clear_text("device123")

        assert result.success is True


class TestUIHierarchy:
    """Tests for UI hierarchy operations."""

    @respx.mock
    def test_dump_hierarchy(self) -> None:
        response_data = {"nodes": [{"id": 1, "text": "Button"}]}
        _ = respx.post("https://api.devicebase.cn/v1/dump_hierarchy/device123").mock(
            return_value=httpx.Response(200, json=response_data)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            info = client.dump_hierarchy("device123")

        assert info.data == response_data


class TestScreenshots:
    """Tests for screenshot APIs."""

    @respx.mock
    def test_get_screenshot(self) -> None:
        jpeg_data = b"fake-jpeg-data"
        _ = respx.get("https://api.devicebase.cn/v1/screen/device123").mock(
            return_value=httpx.Response(200, content=jpeg_data)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.get_screenshot("device123")

        assert result == jpeg_data

    @respx.mock
    def test_get_screenshot_post(self) -> None:
        jpeg_data = b"fake-jpeg-data"
        _ = respx.post("https://api.devicebase.cn/v1/screen/device123").mock(
            return_value=httpx.Response(200, content=jpeg_data)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.get_screenshot_post("device123")

        assert result == jpeg_data

    @respx.mock
    def test_download_screenshot(self) -> None:
        jpeg_data = b"fake-jpeg-data"
        _ = respx.get("https://api.devicebase.cn/v1/screenshot/device123").mock(
            return_value=httpx.Response(200, content=jpeg_data)
        )

        with DeviceBaseHttpClient(api_key="test-key") as client:
            result = client.download_screenshot("device123")

        assert result == jpeg_data
