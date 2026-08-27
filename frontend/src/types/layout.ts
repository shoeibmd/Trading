import { Layout } from 'react-grid-layout';
import { PanelConfiguration } from './panel';

export interface PanelLayout {
  panelInstanceId: string; // Unique instance ID
  panelDefinitionId: string; // Reference to PanelDefinition.id
  configuration: PanelConfiguration;
  layout: Layout; // React Grid Layout position/size
}

export interface WorkspaceLayout {
  workspaceId: string;
  panels: PanelLayout[];
}

export interface Workspace {
  id: string;
  userId: string;
  name: string;
  description?: string;
  isDefault: boolean;
  layout: WorkspaceLayout;
  createdAt: string;
  updatedAt: string;
}

export interface CreateWorkspaceDto {
  name: string;
  description?: string;
  isDefault?: boolean;
  layout?: WorkspaceLayout;
}

export interface UpdateWorkspaceDto {
  name?: string;
  description?: string;
  isDefault?: boolean;
  layout?: WorkspaceLayout;
}
