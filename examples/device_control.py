"""Device control: info, touch, navigation, and text input."""

from devicebase import DeviceBaseClient

# Initialize client (reads DEVICEBASE_API_KEY from environment)
client = DeviceBaseClient()

device = "device123"

# === Device Info ===
info = client.get_device_info(device)
print(f"Device: {info.data['data']}")

# === Touch Operations ===
client.tap(device, x=540, y=960)  # Single tap at center-bottom
client.double_tap(device, x=540, y=960)  # Double tap
client.long_press(device, x=540, y=960)  # Long press (opens context menu)
client.swipe(device, x1=540, y1=1600, x2=540, y2=400)  # Swipe up

# === Navigation ===
client.back(device)  # Press back button
client.home(device)  # Press home button

# === App Operations ===
client.launch_app(device, "华为商城")  # Launch Huawei Mall
app_info = client.get_current_app(device) 
print(f"Foreground app: {app_info.data['data'].get('app_name')}")

# === Text Input ===
client.input_text(device, "Hello World")  # Type text
client.clear_text(device)  # Clear text field

client.close()
