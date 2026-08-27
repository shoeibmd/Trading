import { WorkspaceLayout, PanelLayout } from '../types/layout';
import { panelRegistry } from '../services/panelRegistry';

/**
 * Validates and attempts to auto-fix a workspace layout configuration.
 * Removes panels that reference non-existent definitions.
 * Ensures basic layout bounds exist.
 */
export function validateAndFixLayout(layout: WorkspaceLayout): WorkspaceLayout {
  if (!layout || !layout.panels) {
    return { workspaceId: layout?.workspaceId || '', panels: [] };
  }

  const fixedPanels: PanelLayout[] = [];

  for (const panel of layout.panels) {
    // 1. Check for missing panel definitions
    const def = panelRegistry.get(panel.panelDefinitionId);
    if (!def) {
      console.warn(`Panel definition ${panel.panelDefinitionId} not found. Removing from layout.`);
      continue;
    }

    // 2. Validate/Fix Layout coordinates
    let l = panel.layout;
    if (!l) {
      l = { i: panel.panelInstanceId, x: 0, y: Infinity, w: 4, h: 4 };
    } else {
      // Ensure required properties exist
      l = {
        i: l.i || panel.panelInstanceId,
        x: typeof l.x === 'number' ? l.x : 0,
        y: typeof l.y === 'number' ? l.y : Infinity, // Infinity puts it at the bottom
        w: typeof l.w === 'number' ? l.w : 4,
        h: typeof l.h === 'number' ? l.h : 4,
        minW: l.minW,
        maxW: l.maxW,
        minH: l.minH,
        maxH: l.maxH,
      };
    }

    // 3. Ensure configuration object exists
    const config = panel.configuration || {};

    fixedPanels.push({
      ...panel,
      layout: l,
      configuration: config
    });
  }

  return {
    ...layout,
    panels: fixedPanels
  };
}
