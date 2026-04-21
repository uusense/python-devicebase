"""DeviceBase Python SDK for TestClaw device automation."""

from devicebase.client import DeviceBaseClient
from devicebase.http_client import (
    AuthenticationError,
    DeviceBaseError,
    DeviceNotFoundError,
    ValidationError,
)
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
from devicebase.websocket_client import MinicapClient, MinitouchClient

__version__ = "2026.4.21"

__all__ = [
    # Main client
    "DeviceBaseClient",
    # Exceptions
    "AuthenticationError",
    "DeviceBaseError",
    "DeviceNotFoundError",
    "ValidationError",
    # Models
    "AppInfo",
    "Bounds",
    "DeviceInfo",
    "HierarchyInfo",
    "InputTextRequest",
    "LaunchAppRequest",
    "OperationResult",
    "Point",
    # WebSocket clients
    "MinicapClient",
    "MinitouchClient",
]
