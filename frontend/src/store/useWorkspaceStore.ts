import { create } from 'zustand';
import { Layout } from 'react-grid-layout';
import { Workspace, PanelLayout } from '../types/layout';
import { PanelConfiguration } from '../types/panel';
import { workspaceApi } from '../services/workspaceApi';
import { validateAndFixLayout } from '../utils/layoutValidator';

interface WorkspaceState {
  workspaces: Workspace[];
  activeWorkspaceId: string | null;
  isLoading: boolean;
  error: string | null;

  loadWorkspaces: () => Promise<void>;
  setActiveWorkspace: (id: string) => void;
  addWorkspace: (name: string, description?: string, isDefault?: boolean) => Promise<Workspace | null>;
  updateWorkspace: (id: string, updates: Partial<Workspace>) => Promise<void>;
  deleteWorkspace: (id: string) => Promise<void>;
  addPanelToWorkspace: (workspaceId: string, panelDefId: string, config: PanelConfiguration, layout: Layout) => void;
  removePanelFromWorkspace: (workspaceId: string, panelInstanceId: string) => void;
  updatePanelLayouts: (workspaceId: string, layouts: Layout[]) => void;
  updatePanelConfiguration: (workspaceId: string, panelInstanceId: string, config: PanelConfiguration) => void;
}

let saveTimeout: NodeJS.Timeout | null = null;

export const useWorkspaceStore = create<WorkspaceState>((set, get) => ({
  workspaces: [],
  activeWorkspaceId: null,
  isLoading: false,
  error: null,

  loadWorkspaces: async () => {
    set({ isLoading: true, error: null });
    try {
      let workspaces = await workspaceApi.getWorkspaces();

      if (workspaces.length === 0) {
        const defaultWb = await workspaceApi.createWorkspace({
          name: 'Default Workspace',
          description: 'Your default trading view',
          isDefault: true,
          layout: { workspaceId: '', panels: [] }
        });
        defaultWb.layout.workspaceId = defaultWb.id;
        await workspaceApi.updateWorkspace(defaultWb.id, { layout: defaultWb.layout });
        workspaces = [defaultWb];
      }

      // Run Layout Validator on load
      const validatedWorkspaces = workspaces.map(w => ({
        ...w,
        layout: validateAndFixLayout(w.layout)
      }));

      const active = validatedWorkspaces.find(w => w.isDefault) || validatedWorkspaces[0];
      set({
        workspaces: validatedWorkspaces,
        activeWorkspaceId: active.id,
        isLoading: false
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to load workspaces',
        isLoading: false
      });
    }
  },

  setActiveWorkspace: (id: string) => {
    set({ activeWorkspaceId: id });
  },

  addWorkspace: async (name: string, description?: string, isDefault?: boolean) => {
    try {
      const newWb = await workspaceApi.createWorkspace({
        name,
        description,
        isDefault: isDefault || false,
        layout: { workspaceId: '', panels: [] }
      });
      newWb.layout.workspaceId = newWb.id;

      set(state => ({
        workspaces: [...state.workspaces, newWb],
        activeWorkspaceId: newWb.id
      }));
      return newWb;
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to create workspace' });
      return null;
    }
  },

  updateWorkspace: async (id: string, updates: Partial<Workspace>) => {
    set(state => ({
      workspaces: state.workspaces.map(w => w.id === id ? { ...w, ...updates } : w)
    }));

    try {
      await workspaceApi.updateWorkspace(id, updates);
    } catch (error) {
      console.error('Failed to update workspace API:', error);
    }
  },

  deleteWorkspace: async (id: string) => {
    try {
      await workspaceApi.deleteWorkspace(id);
      set(state => {
        const newWorkspaces = state.workspaces.filter(w => w.id !== id);
        const newActive = state.activeWorkspaceId === id
          ? (newWorkspaces.find(w => w.isDefault)?.id || (newWorkspaces.length > 0 ? newWorkspaces[0].id : null))
          : state.activeWorkspaceId;

        return {
          workspaces: newWorkspaces,
          activeWorkspaceId: newActive
        };
      });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to delete workspace' });
    }
  },

  addPanelToWorkspace: (workspaceId: string, panelDefId: string, config: PanelConfiguration, layout: Layout) => {
    const { workspaces } = get();
    const workspace = workspaces.find(w => w.id === workspaceId);
    if (!workspace) return;

    const instanceId = `panel-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const newPanel: PanelLayout = {
      panelInstanceId: instanceId,
      panelDefinitionId: panelDefId,
      configuration: config,
      layout: { ...layout, i: instanceId } // Ensure the react-grid-layout gets the exact instance ID
    };

    const updatedLayout = {
      ...workspace.layout,
      panels: [...(workspace.layout.panels || []), newPanel]
    };

    set(state => ({
      workspaces: state.workspaces.map(w =>
        w.id === workspaceId ? { ...w, layout: updatedLayout } : w
      )
    }));

    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
      workspaceApi.updateWorkspace(workspaceId, { layout: updatedLayout }).catch(console.error);
    }, 500);
  },

  removePanelFromWorkspace: (workspaceId: string, panelInstanceId: string) => {
    const { workspaces } = get();
    const workspace = workspaces.find(w => w.id === workspaceId);
    if (!workspace) return;

    const updatedLayout = {
      ...workspace.layout,
      panels: workspace.layout.panels.filter(p => p.panelInstanceId !== panelInstanceId)
    };

    set(state => ({
      workspaces: state.workspaces.map(w =>
        w.id === workspaceId ? { ...w, layout: updatedLayout } : w
      )
    }));

    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
      workspaceApi.updateWorkspace(workspaceId, { layout: updatedLayout }).catch(console.error);
    }, 500);
  },

  updatePanelLayouts: (workspaceId: string, layouts: Layout[]) => {
    const { workspaces } = get();
    const workspace = workspaces.find(w => w.id === workspaceId);
    if (!workspace) return;

    const updatedPanels = workspace.layout.panels.map(panel => {
      const newLayout = layouts.find(l => l.i === panel.panelInstanceId);
      return newLayout ? { ...panel, layout: newLayout } : panel;
    });

    const updatedLayout = { ...workspace.layout, panels: updatedPanels };

    set(state => ({
      workspaces: state.workspaces.map(w =>
        w.id === workspaceId ? { ...w, layout: updatedLayout } : w
      )
    }));

    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
      workspaceApi.updateWorkspace(workspaceId, { layout: updatedLayout }).catch(console.error);
    }, 500);
  },

  updatePanelConfiguration: (workspaceId: string, panelInstanceId: string, config: PanelConfiguration) => {
    const { workspaces } = get();
    const workspace = workspaces.find(w => w.id === workspaceId);
    if (!workspace) return;

    const updatedPanels = workspace.layout.panels.map(panel =>
      panel.panelInstanceId === panelInstanceId ? { ...panel, configuration: config } : panel
    );

    const updatedLayout = { ...workspace.layout, panels: updatedPanels };

    set(state => ({
      workspaces: state.workspaces.map(w =>
        w.id === workspaceId ? { ...w, layout: updatedLayout } : w
      )
    }));

    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
      workspaceApi.updateWorkspace(workspaceId, { layout: updatedLayout }).catch(console.error);
    }, 500);
  }
}));
