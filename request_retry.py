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
                    # print(f"{func.__name__} succeeded.") # only for debugging
                    return result
                except Exception as e:
                    attempts += 1
                    if 'is unavailable' in str(e) or 'member' in str(e) or 'streamingData' in str(e):
                        print("no authority to access, skip ...")
                        break
                    elif 'Subtitles are disabled' in str(e):
                        print('Subtitles are disabled for this video ...')
                        break
                    elif max_attempts is not None and attempts >= max_attempts:
                        print(f"{func.__name__} failed after {attempts} attempts: {e}")
                        break
                    elif 'IncompleteRead' in str(e):  
                        _sleep_time = 0
                    elif 'HTTP Error 429' in str(e):  
                        _sleep_time = sleep_time
                    else:
                        print('unknown exception to check ...')
                        _sleep_time = 0

                    print(f"{func.__name__} failed on attempt {attempts}: {e}")
                    for wait in range(_sleep_time):
                        print(wait, end=' ')
                        time.sleep(1)
        return wrapper
    return decorator
