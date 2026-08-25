import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore } from '../store/useAppStore';

describe('useAppStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useAppStore.setState({
      activeWorkspaceId: null,
      theme: 'dark',
      isLoading: false,
      globalError: null,
    });
  });

  it('should initialize with default values', () => {
    const state = useAppStore.getState();
    expect(state.activeWorkspaceId).toBeNull();
    expect(state.theme).toBe('dark');
    expect(state.isLoading).toBe(false);
  });

  it('should toggle theme correctly', () => {
    const store = useAppStore.getState();
    store.toggleTheme();
    expect(useAppStore.getState().theme).toBe('light');
    store.toggleTheme();
    expect(useAppStore.getState().theme).toBe('dark');
  });

  it('should set active workspace id', () => {
    const store = useAppStore.getState();
    store.setActiveWorkspaceId('ws-123');
    expect(useAppStore.getState().activeWorkspaceId).toBe('ws-123');
  });
});
