import React, { useState } from 'react';
import { EmptyState } from '../components/states/EmptyState';
import { Plus } from 'lucide-react';
import { Button } from '../components/ui/button';
import { PanelContainer } from '../components/panels/PanelContainer';
import { panelRegistry } from '../services/panelRegistry';
import { getDefaultConfiguration, generatePanelId } from '../utils/panelUtils';

interface ActivePanel {
  id: string; // unique instance id
  definitionId: string; // registry definition id
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  configuration: any;
}

export const MainWorkspace: React.FC = () => {
  const [activePanels, setActivePanels] = useState<ActivePanel[]>([]);

  const handleAddTestPanel = () => {
    const testPanelDef = panelRegistry.get('test-panel');
    if (!testPanelDef) return;

    const newPanel: ActivePanel = {
      id: generatePanelId(),
      definitionId: testPanelDef.id,
      configuration: getDefaultConfiguration(testPanelDef.configurationSchema)
    };

    setActivePanels(prev => [...prev, newPanel]);
  };

  const handleClosePanel = (panelId: string) => {
    setActivePanels(prev => prev.filter(p => p.id !== panelId));
  };

  return (
    <div className="flex-1 bg-muted/20 relative overflow-hidden flex flex-col h-full" data-testid="main-workspace">
      {/* Workspace Toolbar */}
      <div className="h-12 border-b flex items-center justify-between px-4 bg-background">
        <h2 className="text-sm font-semibold">Default Workspace</h2>
        <div className="flex items-center gap-2">
          <Button size="sm" onClick={handleAddTestPanel} className="h-8 gap-2">
            <Plus className="h-4 w-4" />
            Add Test Panel
          </Button>
        </div>
      </div>

      {/* Workspace Content */}
      <div className="flex-1 overflow-auto p-4">
        {activePanels.length === 0 ? (
          <EmptyState
            title="Workspace is empty"
            description="Add panels to start building your terminal"
            action={{ label: "Add Panel", onClick: handleAddTestPanel }}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 auto-rows-[300px]">
            {activePanels.map(panel => {
              const definition = panelRegistry.get(panel.definitionId);
              if (!definition) return null;

              return (
                <div key={panel.id} className="h-full w-full">
                  <PanelContainer
                    panelId={panel.id}
                    definition={definition}
                    initialConfiguration={panel.configuration}
                    onClose={handleClosePanel}
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
