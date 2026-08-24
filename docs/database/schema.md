# Database Schema

## Overview
The database uses PostgreSQL for relational data and TimescaleDB for time-series data.

## Core Entities
- **Users**: Application users and their roles (`users`).
- **Exchanges**: Financial exchanges (`exchanges`).
- **Instruments**: Tradable financial assets (`instruments`).
- **Workspaces & Panels**: User UI configuration (`workspaces`, `workspace_panels`).
- **Watchlists & Items**: User instrument tracking lists (`watchlists`, `watchlist_items`).
- **Portfolios, Positions, Transactions**: User financial positions (`portfolios`, `portfolio_positions`, `portfolio_transactions`).
- **News**: Financial news and associated instrument relevancy (`news_articles`, `news_article_instruments`).
- **Fundamentals**: Key financial indicators per instrument (`fundamentals`).
- **Providers**: Third-party data providers mapping (`market_data_providers`, `provider_symbols`).

## Time-Series Entities (TimescaleDB Hypertables)
- **Quotes**: Granular quote data chunked by `time`.
- **OHLCV**: Aggregated time-based interval pricing chunked by `time`.

## Indexing Strategy
- Heavy use of composite indexes on Time-Series data (e.g. `(instrument_id, time DESC)` on quotes).
- Strict cascading foreign keys logic on deletions to prevent orphans.
