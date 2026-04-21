"""Error handling and recovery patterns."""

import time

from devicebase import (
    DeviceBaseClient,
    AuthenticationError,
    DeviceNotFoundError,
    ValidationError,
    DeviceBaseError,
)


def demonstrate_error_handling():
    """Show different error types and handling patterns."""

    try:
        # Missing API key
        client = DeviceBaseClient(serial="device123", api_key="invalid-key")
    except AuthenticationError as e:
        print(f"Auth failed: {e.message}")

    try:
        client = DeviceBaseClient(serial="device123")  # Uses env var
        client.get_device_info()
    except DeviceNotFoundError as e:
        print(f"Device not found: {e.message}")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
    except DeviceBaseError as e:
        print(f"API error {e.status_code}: {e.message}")


def retry_pattern(max_retries: int = 3, delay: float = 1.0):
    """Retry device operations with exponential backoff."""

    client = DeviceBaseClient(serial="device123")

    for attempt in range(max_retries):
        try:
            info = client.get_device_info()
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


if __name__ == "__main__":
    print("=== Error Handling ===")
    demonstrate_error_handling()

    print("\n=== Retry Pattern ===")
    # retry_pattern()  # Uncomment when devices are available
