import time


def send(client, to, template, params):
    return client.send(to=to, template=template, params=params)


def send_with_retry(client, to, template, params, attempts=3, backoff=1, sleep=time.sleep):
    """Send an email, retrying on transient provider errors.

    Retries up to `attempts` times with exponential backoff
    (backoff * 2**n seconds between attempts). `sleep` is injectable
    so tests don't need to actually wait.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    last_error = None
    for attempt in range(attempts):
        try:
            return send(client, to, template, params)
        except Exception as exc:  # noqa: BLE001 - provider SDK can raise various errors
            last_error = exc
            if attempt < attempts - 1:
                sleep(backoff * (2 ** attempt))

    raise last_error
