import time

def retry(max_attempts=None, sleep_time=0):
    """
    Decorator that retries the wrapped function `max_attempts` times, with a delay of `sleep_time` seconds between retries.
    If `max_attempts` is not specified or is None, retries indefinitely.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    print(f"{func.__name__} succeeded.")
                    return result
                except Exception as e:
                    attempts += 1
                    if max_attempts is not None and attempts >= max_attempts:
                        print(f"{func.__name__} failed after {attempts} attempts: {e}")
                        break
                    print(f"{func.__name__} failed on attempt {attempts}: {e}")
                    print(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
        return wrapper
    return decorator
