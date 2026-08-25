import React from 'react';

export type PanelCategory =
  | 'market'
  | 'stock'
  | 'technical'
  | 'news'
  | 'fundamentals'
  | 'portfolio'
  | 'ai'
  | 'utility';

export type PanelSize = 'small' | 'medium' | 'large' | 'xlarge';

export interface DataRequirement {
  type: 'quote' | 'ohlcv' | 'instrument' | 'news' | 'fundamental' | 'portfolio';
  instrumentId?: string;
  interval?: string;
  limit?: number;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export interface PanelConfiguration {
  [key: string]: any; // Panel-specific configuration
}

export interface PanelState {
  status: 'loading' | 'empty' | 'error' | 'success';
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data?: any;
  error?: string;
  lastUpdated?: Date;
}

export interface PanelProps {
  panelId: string;
  configuration: PanelConfiguration;
  onConfigurationChange: (config: PanelConfiguration) => void;
  onClose: () => void;
  onRefresh: () => void;
}

export interface PanelDefinition {
  id: string;
  type: string;
  title: string;
  category: PanelCategory;
  description: string;
  defaultSize: PanelSize;
  icon?: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  configurationSchema?: any; // JSON Schema for configuration UI
  dataRequirements: DataRequirement[];
  component: React.ComponentType<PanelProps>;
}
