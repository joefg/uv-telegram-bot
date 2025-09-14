import pytest
import models.ping

def test_ping_always_returns_pong():
    ret = models.ping.ping()
    assert ret == "Pong!"
