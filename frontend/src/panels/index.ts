import { panelRegistry } from '../services/panelRegistry';
import { testPanelDefinition } from '../components/panels/examples/TestPanel';
import { marketOverviewPanelDefinition } from '../components/panels/market/MarketOverviewPanel';
import { topGainersPanelDefinition } from '../components/panels/market/TopGainersPanel';
import { topLosersPanelDefinition } from '../components/panels/market/TopLosersPanel';
import { mostActivePanelDefinition } from '../components/panels/market/MostActivePanel';
import { marketBreadthPanelDefinition } from '../components/panels/market/MarketBreadthPanel';
import { watchlistPanelDefinition } from '../components/panels/market/WatchlistPanel';

export function initializePanels() {
  try {
    // Phase 9 panels
    panelRegistry.register(testPanelDefinition);

    // Phase 11 panels
    panelRegistry.register(marketOverviewPanelDefinition);
    panelRegistry.register(topGainersPanelDefinition);
    panelRegistry.register(topLosersPanelDefinition);
    panelRegistry.register(mostActivePanelDefinition);
    panelRegistry.register(marketBreadthPanelDefinition);
    panelRegistry.register(watchlistPanelDefinition);

    console.log('Panels initialized successfully.');
  } catch (error) {
    console.error('Failed to initialize panels:', error);
  }
}
