import { PanelDefinition, PanelCategory } from '../types/panel';

class PanelRegistry {
  private panels: Map<string, PanelDefinition> = new Map();

  register(panel: PanelDefinition): void {
    if (this.panels.has(panel.id)) {
      throw new Error(`Panel ${panel.id} already registered`);
    }
    this.panels.set(panel.id, panel);
  }

  get(id: string): PanelDefinition | undefined {
    return this.panels.get(id);
  }

  getAll(): PanelDefinition[] {
    return Array.from(this.panels.values());
  }

  getByCategory(category: PanelCategory): PanelDefinition[] {
    return this.getAll().filter(p => p.category === category);
  }

  unregister(id: string): void {
    this.panels.delete(id);
  }
}

export const panelRegistry = new PanelRegistry();
