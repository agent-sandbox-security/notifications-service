import pytest

from src.mailer import send_with_retry


class FakeClient:
    def __init__(self, fail_times=0, exc=RuntimeError("transient error")):
        self.fail_times = fail_times
        self.exc = exc
        self.calls = 0

    def send(self, to, template, params):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise self.exc
        return {"to": to, "template": template, "params": params}


def test_send_with_retry_succeeds_first_try():
    client = FakeClient(fail_times=0)
    sleeps = []

    result = send_with_retry(
        client, "a@example.com", "welcome", {}, attempts=3, sleep=sleeps.append
    )

    assert result == {"to": "a@example.com", "template": "welcome", "params": {}}
    assert client.calls == 1
    assert sleeps == []


def test_send_with_retry_succeeds_after_transient_failures():
    client = FakeClient(fail_times=2)
    sleeps = []

    result = send_with_retry(
        client, "a@example.com", "welcome", {}, attempts=3, backoff=1, sleep=sleeps.append
    )

    assert result == {"to": "a@example.com", "template": "welcome", "params": {}}
    assert client.calls == 3
    # exponential backoff: 1*2**0, 1*2**1
    assert sleeps == [1, 2]


def test_send_with_retry_raises_after_exhausting_attempts():
    client = FakeClient(fail_times=5)
    sleeps = []

    with pytest.raises(RuntimeError, match="transient error"):
        send_with_retry(
            client, "a@example.com", "welcome", {}, attempts=3, sleep=sleeps.append
        )

    assert client.calls == 3
    assert sleeps == [1, 2]


def test_send_with_retry_invalid_attempts():
    client = FakeClient()

    with pytest.raises(ValueError):
        send_with_retry(client, "a@example.com", "welcome", {}, attempts=0)
