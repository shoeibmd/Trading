import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin

class Watchlist(Base, TimestampMixin):
    """
    User watchlist.
    """
    __tablename__ = "watchlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)

    user = relationship("User", backref="watchlists")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan", order_by="WatchlistItem.order")

    def __repr__(self) -> str:
        return f"<Watchlist {self.name} (id={self.id})>"

class WatchlistItem(Base, TimestampMixin):
    """
    An instrument in a watchlist.
    """
    __tablename__ = "watchlist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    watchlist_id = Column(UUID(as_uuid=True), ForeignKey('watchlists.id', ondelete='CASCADE'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id', ondelete='CASCADE'), nullable=False)
    order = Column(Integer, nullable=False, default=0)

    watchlist = relationship("Watchlist", back_populates="items")
    instrument = relationship("Instrument")

    def __repr__(self) -> str:
        return f"<WatchlistItem instrument={self.instrument_id} (order={self.order})>"
