from sqlalchemy import func
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, Enum, Text,
    Integer, Numeric, BigInteger, UniqueConstraint, Index, Date, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, date
from .base import Base, TimestampMixin, UUIDMixin
import enum

class InstrumentType(str, enum.Enum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    INDEX = "INDEX"
    BOND = "BOND"
    DERIVATIVE = "DERIVATIVE"
    CURRENCY = "CURRENCY"

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class TransactionType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"

class ProviderType(str, enum.Enum):
    REST_API = "REST_API"
    WEBSOCKET = "WEBSOCKET"
    FILE = "FILE"
    MANUAL = "MANUAL"

class Exchange(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "exchanges"

    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    timezone: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    instruments = relationship("Instrument", back_populates="exchange", cascade="all, delete-orphan")

class Instrument(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "instruments"
    __table_args__ = (
        UniqueConstraint('exchange_id', 'symbol', name='uq_exchange_symbol'),
        Index('ix_instrument_symbol', 'symbol'),
        Index('ix_instrument_isin', 'isin'),
        Index('ix_instrument_type', 'instrument_type'),
        Index('ix_instrument_active', 'is_active'),
    )

    exchange_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('exchanges.id', ondelete='CASCADE'))
    symbol: Mapped[str] = mapped_column(String)
    isin: Mapped[str] = mapped_column(String, nullable=True)
    instrument_type: Mapped[InstrumentType] = mapped_column(Enum(InstrumentType))
    name: Mapped[str] = mapped_column(String)
    sector: Mapped[str] = mapped_column(String, nullable=True)
    industry: Mapped[str] = mapped_column(String, nullable=True)
    lot_size: Mapped[int] = mapped_column(Integer, default=1)
    tick_size: Mapped[float] = mapped_column(Numeric)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    exchange = relationship("Exchange", back_populates="instruments")
    fundamentals = relationship("Fundamental", back_populates="instrument", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="instrument", cascade="all, delete-orphan")
    ohlcv = relationship("OHLCV", back_populates="instrument", cascade="all, delete-orphan")

class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index('ix_user_email', 'email'),
        Index('ix_user_username', 'username'),
        Index('ix_user_active', 'is_active'),
    )

    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    last_login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    workspaces = relationship("Workspace", back_populates="user", cascade="all, delete-orphan")
    watchlists = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")

class Workspace(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "workspaces"
    __table_args__ = (Index('ix_workspace_user', 'user_id'),)

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    layout_config: Mapped[dict] = mapped_column(JSONB, default=dict)

    user = relationship("User", back_populates="workspaces")
    panels = relationship("WorkspacePanel", back_populates="workspace", cascade="all, delete-orphan")

class WorkspacePanel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "workspace_panels"
    __table_args__ = (Index('ix_panel_workspace', 'workspace_id'),)

    workspace_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'))
    panel_type: Mapped[str] = mapped_column(String)
    panel_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    z_index: Mapped[int] = mapped_column(Integer, default=0)

    workspace = relationship("Workspace", back_populates="panels")

class Watchlist(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "watchlists"
    __table_args__ = (Index('ix_watchlist_user', 'user_id'),)

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="watchlists")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")

class WatchlistItem(Base, UUIDMixin):
    __tablename__ = "watchlist_items"
    __table_args__ = (
        UniqueConstraint('watchlist_id', 'instrument_id', name='uq_watchlist_instrument'),
        Index('ix_watchlist_item_watchlist', 'watchlist_id'),
        Index('ix_watchlist_item_instrument', 'instrument_id'),
    )

    watchlist_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('watchlists.id', ondelete='CASCADE'))
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'))
    position: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    watchlist = relationship("Watchlist", back_populates="items")
    instrument = relationship("Instrument")

class Quote(Base):
    __tablename__ = "quotes"
    __table_args__ = (
        Index('ix_quotes_instrument_time', 'instrument_id', 'time', postgresql_ops={'time': 'DESC'}),
        Index('ix_quotes_source', 'source'),
    )

    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    bid_price: Mapped[float] = mapped_column(Numeric, nullable=True)
    ask_price: Mapped[float] = mapped_column(Numeric, nullable=True)
    last_price: Mapped[float] = mapped_column(Numeric, nullable=True)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=True)
    bid_size: Mapped[int] = mapped_column(BigInteger, nullable=True)
    ask_size: Mapped[int] = mapped_column(BigInteger, nullable=True)
    source: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    instrument = relationship("Instrument", back_populates="quotes")

class OHLCV(Base):
    __tablename__ = "ohlcv"
    __table_args__ = (
        Index('ix_ohlcv_instrument_interval_time', 'instrument_id', 'interval', 'time', postgresql_ops={'time': 'DESC'}),
        Index('ix_ohlcv_source', 'source'),
    )

    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    interval: Mapped[str] = mapped_column(String, primary_key=True)
    open: Mapped[float] = mapped_column(Numeric, nullable=True)
    high: Mapped[float] = mapped_column(Numeric, nullable=True)
    low: Mapped[float] = mapped_column(Numeric, nullable=True)
    close: Mapped[float] = mapped_column(Numeric, nullable=True)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=True)
    trades_count: Mapped[int] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    instrument = relationship("Instrument", back_populates="ohlcv")

class Portfolio(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "portfolios"
    __table_args__ = (Index('ix_portfolio_user', 'user_id'),)

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    currency: Mapped[str] = mapped_column(String, default='INR')
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="portfolios")
    positions = relationship("PortfolioPosition", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = relationship("PortfolioTransaction", back_populates="portfolio", cascade="all, delete-orphan")

class PortfolioPosition(Base, UUIDMixin):
    __tablename__ = "portfolio_positions"
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'instrument_id', name='uq_portfolio_instrument'),
        Index('ix_position_portfolio', 'portfolio_id'),
        Index('ix_position_instrument', 'instrument_id'),
    )

    portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'))
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'))
    quantity: Mapped[float] = mapped_column(Numeric)
    average_cost: Mapped[float] = mapped_column(Numeric)
    current_price: Mapped[float] = mapped_column(Numeric, nullable=True)
    unrealized_pnl: Mapped[float] = mapped_column(Numeric, nullable=True)
    realized_pnl: Mapped[float] = mapped_column(Numeric, default=0)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    portfolio = relationship("Portfolio", back_populates="positions")
    instrument = relationship("Instrument")

class PortfolioTransaction(Base, UUIDMixin):
    __tablename__ = "portfolio_transactions"
    __table_args__ = (
        Index('ix_transaction_portfolio', 'portfolio_id'),
        Index('ix_transaction_instrument', 'instrument_id'),
        Index('ix_transaction_date', 'transaction_date'),
    )

    portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'))
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'))
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    quantity: Mapped[float] = mapped_column(Numeric)
    price: Mapped[float] = mapped_column(Numeric)
    fees: Mapped[float] = mapped_column(Numeric, default=0)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="transactions")
    instrument = relationship("Instrument")

class NewsArticle(Base, UUIDMixin):
    __tablename__ = "news_articles"
    __table_args__ = (
        Index('ix_news_published', 'published_at', postgresql_ops={'published_at': 'DESC'}),
        Index('ix_news_source', 'source'),
    )

    title: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String, unique=True)
    source: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    instruments = relationship("NewsArticleInstrument", back_populates="article", cascade="all, delete-orphan")

class NewsArticleInstrument(Base):
    __tablename__ = "news_article_instruments"
    __table_args__ = (
        Index('ix_news_inst_article', 'news_article_id'),
        Index('ix_news_inst_instrument', 'instrument_id'),
    )

    news_article_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('news_articles.id', ondelete='CASCADE'), primary_key=True)
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    relevance_score: Mapped[float] = mapped_column(Numeric, nullable=True)

    article = relationship("NewsArticle", back_populates="instruments")
    instrument = relationship("Instrument")

class Fundamental(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "fundamentals"
    __table_args__ = (
        UniqueConstraint('instrument_id', 'fiscal_year', 'fiscal_quarter', name='uq_fundamental_period'),
        Index('ix_fundamental_instrument', 'instrument_id'),
        Index('ix_fundamental_period', 'period_end_date'),
    )

    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'))
    fiscal_year: Mapped[int] = mapped_column(Integer)
    fiscal_quarter: Mapped[int] = mapped_column(Integer, nullable=True)
    period_end_date: Mapped[date] = mapped_column(Date)
    market_cap: Mapped[int] = mapped_column(BigInteger, nullable=True)
    pe_ratio: Mapped[float] = mapped_column(Numeric, nullable=True)
    pb_ratio: Mapped[float] = mapped_column(Numeric, nullable=True)
    eps: Mapped[float] = mapped_column(Numeric, nullable=True)
    dividend_yield: Mapped[float] = mapped_column(Numeric, nullable=True)
    revenue: Mapped[int] = mapped_column(BigInteger, nullable=True)
    net_income: Mapped[int] = mapped_column(BigInteger, nullable=True)

    instrument = relationship("Instrument", back_populates="fundamentals")

class MarketDataProvider(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "market_data_providers"

    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    provider_type: Mapped[ProviderType] = mapped_column(Enum(ProviderType))
    base_url: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, nullable=True)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)

    symbols = relationship("ProviderSymbol", back_populates="provider", cascade="all, delete-orphan")

class ProviderSymbol(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "provider_symbols"
    __table_args__ = (
        UniqueConstraint('provider_id', 'instrument_id', name='uq_provider_instrument'),
        UniqueConstraint('provider_id', 'provider_symbol', name='uq_provider_symbol_code'),
        Index('ix_provider_symbol_provider', 'provider_id'),
        Index('ix_provider_symbol_instrument', 'instrument_id'),
    )

    provider_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('market_data_providers.id', ondelete='CASCADE'))
    instrument_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'))
    provider_symbol: Mapped[str] = mapped_column(String)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    provider = relationship("MarketDataProvider", back_populates="symbols")
    instrument = relationship("Instrument")
