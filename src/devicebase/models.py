"""Data models for the DeviceBase SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Point:
    """Represents a 2D coordinate point on the device screen.

    Attributes:
        x: Horizontal coordinate (pixels from left).
        y: Vertical coordinate (pixels from top).
    """

    x: int = 0
    y: int = 0

    def to_dict(self) -> dict[str, int]:
        """Convert to dictionary for API requests."""
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Point:
        """Create a Point from a dictionary."""
        return cls(x=data.get("x", 0), y=data.get("y", 0))


@dataclass(frozen=True)
class Bounds:
    """Represents a rectangular area or swipe path on the device screen.

    Attributes:
        x1: Starting x-coordinate (for swipe) or left edge.
        y1: Starting y-coordinate (for swipe) or top edge.
        x2: Ending x-coordinate (for swipe) or right edge.
        y2: Ending y-coordinate (for swipe) or bottom edge.
    """

    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0

    def to_dict(self) -> dict[str, int]:
        """Convert to dictionary for API requests."""
        return {"x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Bounds:
        """Create Bounds from a dictionary."""
        return cls(
            x1=data.get("x1", 0),
            y1=data.get("y1", 0),
            x2=data.get("x2", 0),
            y2=data.get("y2", 0),
        )


@dataclass(frozen=True)
class LaunchAppRequest:
    """Request payload for launching an application.

    Attributes:
        app_name: The package name or identifier of the app to launch.
    """

    app_name: str = ""

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for API requests."""
        return {"app_name": self.app_name}


@dataclass(frozen=True)
class InputTextRequest:
    """Request payload for text input.

    Attributes:
        text: The text string to input into the focused field.
    """

    text: str = ""

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for API requests."""
        return {"text": self.text}


@dataclass(frozen=True)
class DeviceInfo:
    """Device information returned by the API.

    This is a flexible container that adapts to the actual API response structure.
    """

    serial: str
    data: dict[str, Any]

    @classmethod
    def from_dict(cls, serial: str, data: dict[str, Any]) -> DeviceInfo:
        """Create DeviceInfo from API response."""
        return cls(serial=serial, data=data)


@dataclass(frozen=True)
class AppInfo:
    """Information about the currently running application.

    This is a flexible container that adapts to the actual API response structure.
    """

    data: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AppInfo:
        """Create AppInfo from API response."""
        return cls(data=data)


@dataclass(frozen=True)
class HierarchyInfo:
    """UI hierarchy information returned by the API.

    This is a flexible container that adapts to the actual API response structure.
    """

    data: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HierarchyInfo:
        """Create HierarchyInfo from API response."""
        return cls(data=data)


@dataclass(frozen=True)
class OperationResult:
    """Result of a device control operation.

    This is a flexible container that adapts to the actual API response structure.
    """

    success: bool
    data: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OperationResult:
        """Create OperationResult from API response."""
        return cls(success=data.get("success", True), data=data)
