# Devicebase Python SDK

Python SDK for the Devicebase device automation API. Control Android/HarmonyOS/iOS devices programmatically via HTTP and WebSocket interfaces.

## Installation

```bash
pip install devicebase
```

## Quick Start

```python
from devicebase import DeviceBaseClient

# Initialize client with device serial
client = DeviceBaseClient(serial="device123")

# Get device info
info = client.get_device_info()

# Control the device
client.tap(x=100, y=200)
client.swipe(x1=0, y1=500, x2=500, y2=500)
client.launch_app("com.example.app")

# Take a screenshot
screenshot_bytes = client.get_screenshot()
with open("screenshot.jpg", "wb") as f:
    f.write(screenshot_bytes)
```

## Configuration

Configure via environment variables or constructor parameters:

```python
import os

# Option 1: Environment variables (optional, has default values)
os.environ["DEVICEBASE_API_KEY"] = "your-api-key"
# DEVICEBASE_BASE_URL defaults to https://api.devicebase.cn if not set
client = DeviceBaseClient(serial="device123")

# Option 2: Constructor parameters
client = DeviceBaseClient(
    serial="device123",
    base_url="https://api.devicebase.cn",
    api_key="your-api-key"
)
```

Both HTTP and HTTPS protocols are supported.

## Device Control

### Touch Operations

```python
# Single tap
client.tap(x=100, y=200)

# Double tap
client.double_tap(x=100, y=200)

# Long press
client.long_press(x=100, y=200)

# Swipe
client.swipe(x1=0, y1=500, x2=500, y2=500)
```

### Navigation

```python
# Press back button
client.back()

# Press home button
client.home()
```

### App Operations

```python
# Launch an app
client.launch_app("微信")

# Get current foreground app
app_info = client.get_current_app()
print(app_info.data["package"])
```

### Text Input

```python
# Input text into focused field
client.input_text("Hello World")

# Clear text in focused field
client.clear_text()
```

### UI Hierarchy

```python
# Dump UI hierarchy (useful for automation)
hierarchy = client.dump_hierarchy()
print(hierarchy.data)
```

## Screenshots

```python
# Get screenshot as JPEG bytes
screenshot = client.get_screenshot()

# Download screenshot as file attachment
download = client.download_screenshot()
```

## WebSocket Streaming

### Screen Streaming (Minicap)

```python
import asyncio

async def stream_screen():
    client = DeviceBaseClient(serial="device123")
    minicap = client.minicap_client()

    async for frame in minicap.stream_frames():
        # frame is JPEG bytes
        with open("frame.jpg", "wb") as f:
            f.write(frame)

asyncio.run(stream_screen())
```

### Touch Control (Minitouch)

```python
import asyncio

async def control_touch():
    client = DeviceBaseClient(serial="device123")
    minitouch = client.minitouch_client()

    async with minitouch:
        # Tap at coordinates
        await minitouch.tap(100, 200)

        # Swipe gesture
        await minitouch.swipe(0, 500, 500, 500, duration_ms=300)

asyncio.run(control_touch())
```

## Error Handling

```python
from devicebase import (
    DeviceBaseClient,
    AuthenticationError,
    DeviceNotFoundError,
    ValidationError,
)

try:
    client = DeviceBaseClient(serial="device123")
    info = client.get_device_info()
except AuthenticationError:
    print("Invalid or missing API key")
except DeviceNotFoundError:
    print("Device not found or not connected")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Examples

More complete examples can be found in the [examples/](examples/) directory.

- [device_control.py](examples/device_control.py) — Device info, touch, navigation, text input
- [screenshot_hierarchy.py](examples/screenshot_hierarchy.py) — Screenshots and UI hierarchy
- [websocket_minicap.py](examples/websocket_minicap.py) — Real-time screen streaming
- [websocket_minitouch.py](examples/websocket_minitouch.py) — Low-level touch control
- [async_stream.py](examples/async_stream.py) — Async streaming with processing

## License

MIT
