"""Using DeviceBaseClient with context manager (with statement)."""

from devicebase import DeviceBaseClient


def basic_context_manager():
    """Recommended: use with statement for automatic cleanup."""

    with DeviceBaseClient(serial="device123") as client:
        info = client.get_device_info()
        print(f"Device: {info.serial}")

        client.tap(x=540, y=960)

        screenshot = client.get_screenshot()
        print(f"Screenshot: {len(screenshot)} bytes")

    # Client is automatically closed here


def automation_workflow():
    """Example: automated test workflow."""

    with DeviceBaseClient(serial="device123") as client:
        # 1. Check device
        info = client.get_device_info()
        print(f"Starting automation on {info.model}")

        # 2. Launch app
        client.launch_app("com.example.testapp")
        print("App launched")

        # 3. Perform UI actions
        client.tap(x=540, y=960)  # Tap first element
        client.input_text("test input")
        client.tap(x=540, y=1800)  # Tap submit button

        # 4. Take screenshot to verify result
        screenshot = client.get_screenshot()
        with open("result.jpg", "wb") as f:
            f.write(screenshot)
        print("Result screenshot saved")

        # 5. Go back to home
        client.home()
        print("Returned to home")

    # Resources automatically cleaned up


if __name__ == "__main__":
    basic_context_manager()
