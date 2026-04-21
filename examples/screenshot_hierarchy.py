"""Screenshots and UI hierarchy inspection."""

from devicebase import DeviceBaseClient

client = DeviceBaseClient(serial="device123")

# === Screenshots ===
# Get screenshot as raw JPEG bytes
screenshot_bytes = client.get_screenshot()
with open("screenshot.jpg", "wb") as f:
    f.write(screenshot_bytes)

# Download as attachment (with filename)
attachment_bytes = client.download_screenshot()
with open("device123_screenshot.jpg", "wb") as f:
    f.write(attachment_bytes)

# === UI Hierarchy ===
# Dump the current UI element tree
hierarchy = client.dump_hierarchy()
print(f"Hierarchy: {hierarchy.data}")

# === Combine: Screenshot + Hierarchy for automation ===
# Take screenshot before inspecting UI
screenshot = client.get_screenshot()

# Get UI hierarchy to find interactive elements
hierarchy = client.dump_hierarchy()

print(f"Screenshot size: {len(screenshot)} bytes")
print(f"UI tree: {hierarchy.data}")

client.close()
