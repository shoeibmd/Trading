import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { workspaceApi } from '../../services/workspaceApi';

// Mock the API client
vi.mock('../../services/workspaceApi', () => ({
  workspaceApi: {
    getWorkspaces: vi.fn(),
    getWorkspace: vi.fn(),
    createWorkspace: vi.fn(),
    updateWorkspace: vi.fn(),
    deleteWorkspace: vi.fn(),
  }
}));

describe('useWorkspaceStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useWorkspaceStore.setState({
      workspaces: [],
      activeWorkspaceId: null,
      isLoading: false,
      error: null
    });
  });

  it('loads workspaces and creates default if empty', async () => {
    vi.mocked(workspaceApi.getWorkspaces).mockResolvedValue([]);
    vi.mocked(workspaceApi.createWorkspace).mockResolvedValue({
      id: 'default-1',
      userId: 'user',
      name: 'Default Workspace',
      isDefault: true,
      layout: { workspaceId: 'default-1', panels: [] },
      createdAt: '',
      updatedAt: ''
    });

    await useWorkspaceStore.getState().loadWorkspaces();

    expect(workspaceApi.createWorkspace).toHaveBeenCalled();
    expect(useWorkspaceStore.getState().workspaces.length).toBe(1);
    expect(useWorkspaceStore.getState().activeWorkspaceId).toBe('default-1');
  });

  it('sets active workspace to the default one on load', async () => {
    vi.mocked(workspaceApi.getWorkspaces).mockResolvedValue([
      { id: '1', isDefault: false, name: 'w1', userId: 'u', layout: { workspaceId: '1', panels: [] }, createdAt: '', updatedAt: '' },
      { id: '2', isDefault: true, name: 'w2', userId: 'u', layout: { workspaceId: '2', panels: [] }, createdAt: '', updatedAt: '' }
    ]);

    await useWorkspaceStore.getState().loadWorkspaces();

    expect(useWorkspaceStore.getState().workspaces.length).toBe(2);
    expect(useWorkspaceStore.getState().activeWorkspaceId).toBe('2');
  });

  it('adds a panel to a workspace optimistic update', () => {
    // Setup initial state
    useWorkspaceStore.setState({
      workspaces: [{
        id: '1',
        isDefault: true,
        name: 'w1',
        userId: 'u',
        layout: { workspaceId: '1', panels: [] },
        createdAt: '', updatedAt: ''
      }],
      activeWorkspaceId: '1'
    });

    const store = useWorkspaceStore.getState();
    store.addPanelToWorkspace('1', 'test-panel', { message: 'hello' }, { i: 'p1', x: 0, y: 0, w: 2, h: 2 });

    const updatedWorkspace = useWorkspaceStore.getState().workspaces.find(w => w.id === '1');
    expect(updatedWorkspace?.layout.panels.length).toBe(1);
    expect(updatedWorkspace?.layout.panels[0].panelDefinitionId).toBe('test-panel');
  });
});
