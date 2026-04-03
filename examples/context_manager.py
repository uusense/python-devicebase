"""Using DeviceBaseClient with context manager (with statement)."""

from devicebase import DeviceBaseClient

SERIAL = "device123"


def basic_context_manager():
    """Recommended: use with statement for automatic cleanup."""

    with DeviceBaseClient() as client:
        info = client.get_device_info(SERIAL)
        print(f"Device: {info.serial}")

        client.tap(SERIAL, x=540, y=960)

        screenshot = client.get_screenshot(SERIAL)
        print(f"Screenshot: {len(screenshot)} bytes")

    # Client is automatically closed here


def multiple_operations():
    """Batch operations within a single client session."""

    devices = ["device123", "device456"]

    with DeviceBaseClient() as client:
        for serial in devices:
            try:
                info = client.get_device_info(serial)
                print(f"{serial}: {info.status}")
            except Exception as e:
                print(f"{serial}: {e}")

        # Take screenshots of all devices
        for serial in devices:
            try:
                screenshot = client.get_screenshot(serial)
                filename = f"{serial}_screenshot.jpg"
                with open(filename, "wb") as f:
                    f.write(screenshot)
                print(f"Saved: {filename}")
            except Exception as e:
                print(f"Failed to capture {serial}: {e}")


def automation_workflow():
    """Example: automated test workflow."""

    with DeviceBaseClient() as client:
        # 1. Check device
        info = client.get_device_info(SERIAL)
        print(f"Starting automation on {info.model}")

        # 2. Launch app
        client.launch_app(SERIAL, "com.example.testapp")
        print("App launched")

        # 3. Perform UI actions
        client.tap(SERIAL, x=540, y=960)  # Tap first element
        client.input_text(SERIAL, "test input")
        client.tap(SERIAL, x=540, y=1800)  # Tap submit button

        # 4. Take screenshot to verify result
        screenshot = client.get_screenshot(SERIAL)
        with open("result.jpg", "wb") as f:
            f.write(screenshot)
        print("Result screenshot saved")

        # 5. Go back to home
        client.home(SERIAL)
        print("Returned to home")

    # Resources automatically cleaned up


if __name__ == "__main__":
    basic_context_manager()
