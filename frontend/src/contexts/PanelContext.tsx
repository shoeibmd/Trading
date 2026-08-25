import React, { createContext, useContext, ReactNode } from 'react';
import { PanelConfiguration, PanelState } from '../types/panel';

interface PanelContextValue {
  panelId: string;
  configuration: PanelConfiguration;
  state: PanelState;
  onConfigurationChange: (config: PanelConfiguration) => void;
  onRefresh: () => void;
}

const PanelContext = createContext<PanelContextValue | undefined>(undefined);

interface PanelProviderProps {
  children: ReactNode;
  value: PanelContextValue;
}

export const PanelProvider: React.FC<PanelProviderProps> = ({ children, value }) => {
  return (
    <PanelContext.Provider value={value}>
      {children}
    </PanelContext.Provider>
  );
};

export const usePanelContext = (): PanelContextValue => {
  const context = useContext(PanelContext);
  if (!context) {
    throw new Error('usePanelContext must be used within a PanelProvider');
  }
  return context;
};
