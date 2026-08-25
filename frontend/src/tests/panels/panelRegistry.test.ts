import { describe, it, expect, beforeEach } from 'vitest';
import { panelRegistry } from '../../services/panelRegistry';
import { testPanelDefinition } from '../../components/panels/examples/TestPanel';

describe('Panel Registry', () => {
  beforeEach(() => {
    // Clear registry before each test
    const all = panelRegistry.getAll();
    all.forEach(p => panelRegistry.unregister(p.id));
  });

  it('should register a panel successfully', () => {
    panelRegistry.register(testPanelDefinition);
    expect(panelRegistry.get('test-panel')).toBeDefined();
  });

  it('should throw when registering a duplicate panel id', () => {
    panelRegistry.register(testPanelDefinition);
    expect(() => panelRegistry.register(testPanelDefinition)).toThrow();
  });

  it('should retrieve panels by category', () => {
    panelRegistry.register(testPanelDefinition);
    const utilities = panelRegistry.getByCategory('utility');
    const markets = panelRegistry.getByCategory('market');

    expect(utilities.length).toBe(1);
    expect(utilities[0].id).toBe('test-panel');
    expect(markets.length).toBe(0);
  });

  it('should return all registered panels', () => {
    panelRegistry.register(testPanelDefinition);
    expect(panelRegistry.getAll().length).toBe(1);
  });

  it('should unregister a panel successfully', () => {
    panelRegistry.register(testPanelDefinition);
    panelRegistry.unregister('test-panel');
    expect(panelRegistry.get('test-panel')).toBeUndefined();
    expect(panelRegistry.getAll().length).toBe(0);
  });
});
