import os
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mailer import send


@pytest.mark.parametrize("to", ["", None, "no-at-sign"])
def test_send_rejects_invalid_recipient(to):
    client = MagicMock()
    with pytest.raises(ValueError):
        send(client, to, "welcome", {})
    client.send.assert_not_called()


def test_send_passes_valid_recipient_to_client():
    client = MagicMock()
    send(client, "a@example.com", "welcome", {"k": "v"})
    client.send.assert_called_once_with(
        to="a@example.com", template="welcome", params={"k": "v"}
    )
