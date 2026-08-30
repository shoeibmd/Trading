import { panelRegistry } from '../services/panelRegistry';
import { testPanelDefinition } from '../components/panels/examples/TestPanel';
import { marketOverviewPanelDefinition } from '../components/panels/market/MarketOverviewPanel';
import { topGainersPanelDefinition } from '../components/panels/market/TopGainersPanel';
import { topLosersPanelDefinition } from '../components/panels/market/TopLosersPanel';
import { mostActivePanelDefinition } from '../components/panels/market/MostActivePanel';
import { marketBreadthPanelDefinition } from '../components/panels/market/MarketBreadthPanel';
import { watchlistPanelDefinition } from '../components/panels/market/WatchlistPanel';
import { stockOverviewPanelDefinition } from '../components/panels/stock/StockOverviewPanel';
import { stockQuotePanelDefinition } from '../components/panels/stock/StockQuotePanel';
import { stockChartPanelDefinition } from '../components/panels/stock/StockChartPanel';
import { technicalIndicatorsPanelDefinition } from '../components/panels/stock/TechnicalIndicatorsPanel';
import { marketNewsPanelDefinition } from '../components/panels/news/MarketNewsPanel';
import { companyNewsPanelDefinition } from '../components/panels/news/CompanyNewsPanel';
import { newsSearchPanelDefinition } from '../components/panels/news/NewsSearchPanel';
import { newsArticleDetailPanelDefinition } from '../components/panels/news/NewsArticleDetailPanel';

export function initializePanels() {
  try {
    panelRegistry.register(testPanelDefinition);

    // Phase 11
    panelRegistry.register(marketOverviewPanelDefinition);
    panelRegistry.register(topGainersPanelDefinition);
    panelRegistry.register(topLosersPanelDefinition);
    panelRegistry.register(mostActivePanelDefinition);
    panelRegistry.register(marketBreadthPanelDefinition);
    panelRegistry.register(watchlistPanelDefinition);

    // Phase 12
    panelRegistry.register(stockOverviewPanelDefinition);
    panelRegistry.register(stockQuotePanelDefinition);
    panelRegistry.register(stockChartPanelDefinition);
    panelRegistry.register(technicalIndicatorsPanelDefinition);

    // Phase 13
    panelRegistry.register(marketNewsPanelDefinition);
    panelRegistry.register(companyNewsPanelDefinition);
    panelRegistry.register(newsSearchPanelDefinition);
    panelRegistry.register(newsArticleDetailPanelDefinition);

    console.log('Panels initialized successfully.');
  } catch (error) {
    console.error('Failed to initialize panels:', error);
  }
}
