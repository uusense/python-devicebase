"""Tests for DeviceBase SDK models."""

import pytest

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


class TestPoint:
    """Tests for the Point model."""

    def test_default_values(self) -> None:
        point = Point()
        assert point.x == 0
        assert point.y == 0

    def test_custom_values(self) -> None:
        point = Point(x=100, y=200)
        assert point.x == 100
        assert point.y == 200

    def test_to_dict(self) -> None:
        point = Point(x=50, y=75)
        assert point.to_dict() == {"x": 50, "y": 75}

    def test_from_dict(self) -> None:
        data = {"x": 100, "y": 200}
        point = Point.from_dict(data)
        assert point.x == 100
        assert point.y == 200

    def test_from_dict_missing_keys(self) -> None:
        point = Point.from_dict({})
        assert point.x == 0
        assert point.y == 0

    def test_immutable(self) -> None:
        point = Point(x=10, y=20)
        # Frozen dataclass should raise error on modification attempt
        with pytest.raises(AttributeError):
            point.x = 30  # type: ignore[misc]


class TestBounds:
    """Tests for the Bounds model."""

    def test_default_values(self) -> None:
        bounds = Bounds()
        assert bounds.x1 == 0
        assert bounds.y1 == 0
        assert bounds.x2 == 0
        assert bounds.y2 == 0

    def test_custom_values(self) -> None:
        bounds = Bounds(x1=10, y1=20, x2=100, y2=200)
        assert bounds.x1 == 10
        assert bounds.y1 == 20
        assert bounds.x2 == 100
        assert bounds.y2 == 200

    def test_to_dict(self) -> None:
        bounds = Bounds(x1=0, y1=0, x2=100, y2=200)
        assert bounds.to_dict() == {"x1": 0, "y1": 0, "x2": 100, "y2": 200}

    def test_from_dict(self) -> None:
        data = {"x1": 10, "y1": 20, "x2": 100, "y2": 200}
        bounds = Bounds.from_dict(data)
        assert bounds.x1 == 10
        assert bounds.y1 == 20
        assert bounds.x2 == 100
        assert bounds.y2 == 200


class TestLaunchAppRequest:
    """Tests for the LaunchAppRequest model."""

    def test_default_values(self) -> None:
        req = LaunchAppRequest()
        assert req.app_name == ""

    def test_custom_values(self) -> None:
        req = LaunchAppRequest(app_name="com.example.app")
        assert req.app_name == "com.example.app"

    def test_to_dict(self) -> None:
        req = LaunchAppRequest(app_name="com.test.app")
        assert req.to_dict() == {"app_name": "com.test.app"}


class TestInputTextRequest:
    """Tests for the InputTextRequest model."""

    def test_default_values(self) -> None:
        req = InputTextRequest()
        assert req.text == ""

    def test_custom_values(self) -> None:
        req = InputTextRequest(text="Hello World")
        assert req.text == "Hello World"

    def test_to_dict(self) -> None:
        req = InputTextRequest(text="test input")
        assert req.to_dict() == {"text": "test input"}


class TestDeviceInfo:
    """Tests for the DeviceInfo model."""

    def test_from_dict(self) -> None:
        data = {"status": "online", "battery": 85}
        info = DeviceInfo.from_dict("device123", data)
        assert info.serial == "device123"
        assert info.data == data


class TestAppInfo:
    """Tests for the AppInfo model."""

    def test_from_dict(self) -> None:
        data = {"package": "com.example.app", "activity": ".MainActivity"}
        info = AppInfo.from_dict(data)
        assert info.data == data


class TestHierarchyInfo:
    """Tests for the HierarchyInfo model."""

    def test_from_dict(self) -> None:
        data = {"nodes": [{"id": 1, "text": "Button"}]}
        info = HierarchyInfo.from_dict(data)
        assert info.data == data


class TestOperationResult:
    """Tests for the OperationResult model."""

    def test_from_dict_with_success(self) -> None:
        data = {"success": True, "message": "OK"}
        result = OperationResult.from_dict(data)
        assert result.success is True
        assert result.data == data

    def test_from_dict_without_success(self) -> None:
        data = {"message": "OK"}
        result = OperationResult.from_dict(data)
        assert result.success is True  # Default value
        assert result.data == data
