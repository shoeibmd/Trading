import { describe, it, expect, beforeEach, vi } from 'vitest';
import { validateAndFixLayout } from '../../utils/layoutValidator';
import { WorkspaceLayout } from '../../types/layout';
import { panelRegistry } from '../../services/panelRegistry';

// Mock registry
vi.mock('../../services/panelRegistry', () => ({
  panelRegistry: {
    get: vi.fn()
  }
}));

describe('Layout Validator', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('removes panels with missing definitions', () => {
    // Return undefined to simulate missing definition
    vi.mocked(panelRegistry.get).mockReturnValue(undefined);

    const layout: WorkspaceLayout = {
      workspaceId: '1',
      panels: [
        { panelInstanceId: 'p1', panelDefinitionId: 'missing', configuration: {}, layout: { i: 'p1', x: 0, y: 0, w: 2, h: 2 } }
      ]
    };

    const fixed = validateAndFixLayout(layout);
    expect(fixed.panels.length).toBe(0);
  });

  it('fixes missing layout coordinates', () => {
    vi.mocked(panelRegistry.get).mockReturnValue({} as any);

    const layout: WorkspaceLayout = {
      workspaceId: '1',
      panels: [
        { panelInstanceId: 'p1', panelDefinitionId: 'valid', configuration: {}, layout: null as any }
      ]
    };

    const fixed = validateAndFixLayout(layout);
    expect(fixed.panels[0].layout.x).toBe(0);
    expect(fixed.panels[0].layout.y).toBe(Infinity);
    expect(fixed.panels[0].layout.w).toBe(4);
  });
});
