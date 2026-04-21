"""Device control: info, touch, navigation, and text input."""

from devicebase import DeviceBaseClient

# Initialize client (reads DEVICEBASE_API_KEY from environment)
client = DeviceBaseClient(serial="device123")

# === Device Info ===
info = client.get_device_info()
print(f"Device: {info.data['data']}")

# === Touch Operations ===
client.tap(x=540, y=960)  # Single tap at center-bottom
client.double_tap(x=540, y=960)  # Double tap
client.long_press(x=540, y=960)  # Long press (opens context menu)
client.swipe(x1=540, y1=1600, x2=540, y2=400)  # Swipe up

# === Navigation ===
client.back()  # Press back button
client.home()  # Press home button

# === App Operations ===
client.launch_app("华为商城")  # Launch Huawei Mall
app_info = client.get_current_app()
print(f"Foreground app: {app_info.data['data'].get('app_name')}")

# === Text Input ===
client.input_text("Hello World")  # Type text
client.clear_text()  # Clear text field

client.close()
