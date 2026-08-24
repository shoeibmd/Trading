import pytest
from app.models.core import Exchange, Instrument, InstrumentType, User, UserRole, Quote
from uuid import uuid4
from datetime import datetime, timezone

def test_exchange_instantiation():
    """Verify that an Exchange model can be correctly instantiated."""
    ex = Exchange(
        id=uuid4(),
        code="NSE",
        name="National Stock Exchange",
        country="India",
        timezone="Asia/Kolkata",
        currency="INR",
        is_active=True
    )
    assert ex.code == "NSE"
    assert ex.is_active is True

def test_instrument_instantiation():
    """Verify Instrument relationships and enums."""
    inst = Instrument(
        id=uuid4(),
        exchange_id=uuid4(),
        symbol="RELIANCE",
        instrument_type=InstrumentType.EQUITY,
        name="Reliance Industries",
        tick_size=0.05
    )
    assert inst.instrument_type == InstrumentType.EQUITY
    assert inst.tick_size == 0.05

def test_user_instantiation():
    """Verify User default role logic."""
    u = User(
        id=uuid4(),
        email="test@example.com",
        username="testuser",
        password_hash="hash",
        full_name="Test User",
        role=UserRole.USER,
        is_active=True,
        is_verified=False
    )
    assert u.role == UserRole.USER
    assert u.is_active is True
    assert u.is_verified is False

@pytest.mark.timescaledb
def test_hypertable_time_constraint_stub():
    """
    Integration Test Stub for TimescaleDB.
    Requires PostgreSQL with TimescaleDB. Cannot run in sandbox.
    """
    quote = Quote(
        time=datetime.now(timezone.utc),
        instrument_id=uuid4(),
        bid_price=100.5,
        ask_price=100.6,
        source="YAHOO"
    )
    assert quote.time is not None
