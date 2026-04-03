"""Error handling and recovery patterns."""

import time

from devicebase import (
    DeviceBaseClient,
    AuthenticationError,
    DeviceNotFoundError,
    ValidationError,
    DeviceBaseError,
)

SERIAL = "device123"


def demonstrate_error_handling():
    """Show different error types and handling patterns."""

    try:
        # Missing API key
        client = DeviceBaseClient(api_key="invalid-key")
    except AuthenticationError as e:
        print(f"Auth failed: {e.message}")

    try:
        client = DeviceBaseClient()  # Uses env var
        client.get_device_info(SERIAL)
    except DeviceNotFoundError as e:
        print(f"Device not found: {e.message}")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
    except DeviceBaseError as e:
        print(f"API error {e.status_code}: {e.message}")


def retry_pattern(max_retries: int = 3, delay: float = 1.0):
    """Retry device operations with exponential backoff."""

    client = DeviceBaseClient()

    for attempt in range(max_retries):
        try:
            info = client.get_device_info(SERIAL)
            print(f"Device name: {info.data['data']['device']['name']}")
            return info
        except DeviceNotFoundError:
            print(f"Device not ready, attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                raise
        finally:
            client.close()


def retry_with_fallback():
    """Try multiple devices, use first available."""

    devices = ["device123", "device456", "device789"]
    client = DeviceBaseClient()

    for serial in devices:
        try:
            info = client.get_device_info(serial)
            if info.data['data']['device']['is_connected'] == True:
                print(f"Using device: {serial}")
                return serial
        except DeviceNotFoundError:
            continue

    print("No available device found")
    client.close()
    return None


if __name__ == "__main__":
    print("=== Error Handling ===")
    demonstrate_error_handling()

    print("\n=== Retry Pattern ===")
    # retry_pattern()  # Uncomment when devices are available

    print("\n=== Fallback Device ===")
    # device = retry_with_fallback()
