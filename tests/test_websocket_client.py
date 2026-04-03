"""Tests for WebSocket clients."""

import os
from unittest.mock import patch

import pytest

from devicebase.websocket_client import (
    AuthenticationError,
    DeviceBaseError,
    MinicapClient,
    MinitouchClient,
)


class TestMinicapClientInit:
    """Tests for Minicap client initialization."""

    def test_init_with_explicit_params(self) -> None:
        client = MinicapClient(
            base_url="ws://test.com",
            serial="device123",
            api_key="test-key",
        )
        assert client._serial == "device123"
        assert client._api_key == "test-key"
        assert client._url == "ws://test.com/v1/minicap/device123"

    def test_init_converts_http_to_ws(self) -> None:
        client = MinicapClient(
            base_url="http://test.com",
            serial="device123",
            api_key="test-key",
        )
        assert client._url == "ws://test.com/v1/minicap/device123"

    def test_init_with_env_var(self) -> None:
        with patch.dict(os.environ, {"DEVICEBASE_API_KEY": "env-key"}):
            client = MinicapClient(
                base_url="ws://test.com",
                serial="device123",
            )
            assert client._api_key == "env-key"

    def test_init_missing_api_key_raises(self) -> None:
        with patch.dict(os.environ, {}, clear=True), pytest.raises(AuthenticationError):
            MinicapClient(base_url="ws://test.com", serial="device123")


class TestMinitouchClientInit:
    """Tests for Minitouch client initialization."""

    def test_init_with_explicit_params(self) -> None:
        client = MinitouchClient(
            base_url="ws://test.com",
            serial="device123",
            api_key="test-key",
        )
        assert client._serial == "device123"
        assert client._api_key == "test-key"
        assert client._url == "ws://test.com/v1/minitouch/device123"

    def test_init_missing_api_key_raises(self) -> None:
        with patch.dict(os.environ, {}, clear=True), pytest.raises(AuthenticationError):
            MinitouchClient(base_url="ws://test.com", serial="device123")


class TestMinitouchClientConnection:
    """Tests for Minitouch connection management."""

    def test_connect_not_connected_raises(self) -> None:
        client = MinitouchClient(
            base_url="ws://test.com",
            serial="device123",
            api_key="test-key",
        )
        with pytest.raises(DeviceBaseError, match="WebSocket not connected"):
            client._ensure_connected()
