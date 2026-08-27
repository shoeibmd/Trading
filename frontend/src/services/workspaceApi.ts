import { apiClient } from './apiClient';
import { Workspace, CreateWorkspaceDto, UpdateWorkspaceDto } from '../types/layout';

export const workspaceApi = {
  getWorkspaces: async (): Promise<Workspace[]> => {
    const response = await apiClient.get('/api/v1/workspaces/');
    // Handle the APIResponse envelope format -> response.data.data
    const data = response.data.data || response.data;
    return data.map((w: any) => ({
      ...w,
      userId: w.user_id,
      isDefault: w.is_default,
      createdAt: w.created_at,
      updatedAt: w.updated_at,
      layout: w.layout_config
    }));
  },

  getWorkspace: async (id: string): Promise<Workspace> => {
    const response = await apiClient.get(`/api/v1/workspaces/${id}`);
    const w = response.data.data || response.data;
    return {
      ...w,
      userId: w.user_id,
      isDefault: w.is_default,
      createdAt: w.created_at,
      updatedAt: w.updated_at,
      layout: w.layout_config
    };
  },

  createWorkspace: async (data: CreateWorkspaceDto): Promise<Workspace> => {
    const response = await apiClient.post('/api/v1/workspaces/', {
      ...data,
      is_default: data.isDefault,
      layout_config: data.layout
    });
    const w = response.data.data || response.data;
    return {
      ...w,
      userId: w.user_id,
      isDefault: w.is_default,
      createdAt: w.created_at,
      updatedAt: w.updated_at,
      layout: w.layout_config
    };
  },

  updateWorkspace: async (id: string, data: UpdateWorkspaceDto): Promise<void> => {
    await apiClient.patch(`/api/v1/workspaces/${id}`, {
      ...data,
      is_default: data.isDefault,
      layout_config: data.layout
    });
  },

  deleteWorkspace: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/v1/workspaces/${id}`);
  }
};
