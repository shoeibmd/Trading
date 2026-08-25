import React, { useState } from 'react';
import { PanelDefinition, PanelConfiguration, PanelProps } from '../../types/panel';
import { PanelHeader } from './PanelHeader';
import { PanelConfigModal } from './PanelConfigModal';
import { PanelProvider } from '../../contexts/PanelContext';
import { usePanelData } from '../../hooks/usePanelData';
import { PanelLoading } from './states/PanelLoading';
import { PanelError } from './states/PanelError';
import { PanelEmpty } from './states/PanelEmpty';

interface PanelContainerProps {
  panelId: string;
  definition: PanelDefinition;
  initialConfiguration: PanelConfiguration;
  onClose: (panelId: string) => void;
}

export const PanelContainer: React.FC<PanelContainerProps> = ({
  panelId,
  definition,
  initialConfiguration,
  onClose
}) => {
  const [configuration, setConfiguration] = useState<PanelConfiguration>(initialConfiguration);
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const panelState = usePanelData(definition.dataRequirements, configuration, refreshTrigger);

  const handleConfigurationChange = (newConfig: PanelConfiguration) => {
    setConfiguration(newConfig);
  };

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const renderPanelContent = () => {
    if (panelState.status === 'loading') {
      return <PanelLoading />;
    }

    if (panelState.status === 'error') {
      return <PanelError message={panelState.error} onRetry={handleRefresh} />;
    }

    if (panelState.status === 'empty') {
      return <PanelEmpty message="No data available for this configuration." />;
    }

    // Success state - render the actual component
    const Component = definition.component;

    // We pass props directly, but also provide them via context for nested components
    const panelProps: PanelProps = {
      panelId,
      configuration,
      onConfigurationChange: handleConfigurationChange,
      onClose: () => onClose(panelId),
      onRefresh: handleRefresh
    };

    return <Component {...panelProps} />;
  };

  return (
    <PanelProvider
      value={{
        panelId,
        configuration,
        state: panelState,
        onConfigurationChange: handleConfigurationChange,
        onRefresh: handleRefresh
      }}
    >
      <div className="flex flex-col w-full h-full bg-background border rounded-md shadow-sm overflow-hidden" data-testid={`panel-${panelId}`}>
        <PanelHeader
          title={configuration.title || definition.title}
          lastUpdated={panelState.lastUpdated}
          onSettingsClick={() => setIsConfigModalOpen(true)}
          onRefreshClick={handleRefresh}
          onCloseClick={() => onClose(panelId)}
        />

        <div className="flex-1 overflow-auto relative">
          {renderPanelContent()}
        </div>

        <PanelConfigModal
          isOpen={isConfigModalOpen}
          onClose={() => setIsConfigModalOpen(false)}
          configuration={configuration}
          schema={definition.configurationSchema}
          onSave={handleConfigurationChange}
        />
      </div>
    </PanelProvider>
  );
};
