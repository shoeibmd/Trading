import { panelRegistry } from '../services/panelRegistry';
import { testPanelDefinition } from '../components/panels/examples/TestPanel';

/**
 * Initializes the panel framework by registering all available panels.
 * Must be called before rendering the application.
 */
export function initializePanels() {
  try {
    panelRegistry.register(testPanelDefinition);
    // Future panels (market data, charts, etc.) will be registered here
    console.log('Panels initialized successfully.');
  } catch (error) {
    console.error('Failed to initialize panels:', error);
  }
}
