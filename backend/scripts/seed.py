import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models.core import Exchange, Instrument, InstrumentType, MarketDataProvider, ProviderType
from sqlalchemy import select
from uuid import uuid4

async def seed():
    db_url = os.getenv("APP_POSTGRES_DSN", "postgresql+asyncpg://postgres:password@localhost/financial_terminal")
    engine = create_async_engine(db_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Check existing exchanges
        result = await session.execute(select(Exchange).where(Exchange.code.in_(["NSE", "BSE", "NYSE"])))
        existing_exchanges = {ex.code: ex for ex in result.scalars().all()}

        exchanges = []
        if "NSE" not in existing_exchanges:
            exchanges.append(Exchange(id=uuid4(), code="NSE", name="National Stock Exchange", country="India", timezone="Asia/Kolkata", currency="INR"))
        if "BSE" not in existing_exchanges:
            exchanges.append(Exchange(id=uuid4(), code="BSE", name="Bombay Stock Exchange", country="India", timezone="Asia/Kolkata", currency="INR"))
        if "NYSE" not in existing_exchanges:
            exchanges.append(Exchange(id=uuid4(), code="NYSE", name="New York Stock Exchange", country="USA", timezone="America/New_York", currency="USD"))

        if exchanges:
            session.add_all(exchanges)
            await session.commit()
            for ex in exchanges:
                existing_exchanges[ex.code] = ex

        # Check existing providers
        result = await session.execute(select(MarketDataProvider).where(MarketDataProvider.code == "YAHOO_FINANCE"))
        existing_provider = result.scalars().first()

        if not existing_provider:
            provider = MarketDataProvider(id=uuid4(), code="YAHOO_FINANCE", name="Yahoo Finance API", provider_type=ProviderType.REST_API)
            session.add(provider)
            await session.commit()

        # Check existing instruments
        result = await session.execute(select(Instrument).where(Instrument.symbol.in_(["RELIANCE", "TCS", "AAPL"])))
        existing_symbols = {inst.symbol for inst in result.scalars().all()}

        instruments = []
        nse = existing_exchanges.get("NSE")
        nyse = existing_exchanges.get("NYSE")

        if nse and "RELIANCE" not in existing_symbols:
            instruments.append(Instrument(id=uuid4(), exchange_id=nse.id, symbol="RELIANCE", instrument_type=InstrumentType.EQUITY, name="Reliance Industries", tick_size=0.05))
        if nse and "TCS" not in existing_symbols:
            instruments.append(Instrument(id=uuid4(), exchange_id=nse.id, symbol="TCS", instrument_type=InstrumentType.EQUITY, name="Tata Consultancy Services", tick_size=0.05))
        if nyse and "AAPL" not in existing_symbols:
            instruments.append(Instrument(id=uuid4(), exchange_id=nyse.id, symbol="AAPL", instrument_type=InstrumentType.EQUITY, name="Apple Inc.", tick_size=0.01))

        if instruments:
            session.add_all(instruments)
            await session.commit()

        print("Seed data applied successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
