import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Portfolio(Base, TimestampMixin):
    __tablename__ = "portfolios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    currency = Column(String(10), nullable=False, default='USD')
    is_default = Column(Boolean, nullable=False, default=False)

    user = relationship("User", backref="portfolios")
    positions = relationship("PortfolioPosition", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = relationship("PortfolioTransaction", back_populates="portfolio", cascade="all, delete-orphan")


class PortfolioPosition(Base, TimestampMixin):
    __tablename__ = "portfolio_positions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'), nullable=False)

    quantity = Column(Numeric, nullable=False, default=0)
    average_cost = Column(Numeric, nullable=False, default=0)
    realized_pnl = Column(Numeric, nullable=False, default=0)

    portfolio = relationship("Portfolio", back_populates="positions")
    instrument = relationship("Instrument")


class PortfolioTransaction(Base, TimestampMixin):
    __tablename__ = "portfolio_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'), nullable=False)

    transaction_type = Column(String(50), nullable=False) # BUY, SELL, DIVIDEND
    quantity = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    fees = Column(Numeric, nullable=False, default=0)
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(String(500), nullable=True)

    portfolio = relationship("Portfolio", back_populates="transactions")
    instrument = relationship("Instrument")
