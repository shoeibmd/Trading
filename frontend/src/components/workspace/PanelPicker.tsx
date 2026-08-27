import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '../ui/dialog';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { panelRegistry } from '../../services/panelRegistry';
import { getDefaultConfiguration } from '../../utils/panelUtils';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { PanelCategory } from '../../types/panel';

interface PanelPickerProps {
  isOpen: boolean;
  onClose: () => void;
  workspaceId: string;
}

export const PanelPicker: React.FC<PanelPickerProps> = ({ isOpen, onClose, workspaceId }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const { addPanelToWorkspace } = useWorkspaceStore();

  const allPanels = panelRegistry.getAll();

  const filteredPanels = allPanels.filter(p =>
    p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const groupedPanels = filteredPanels.reduce((acc, panel) => {
    const cat = panel.category;
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(panel);
    return acc;
  }, {} as Record<PanelCategory, typeof allPanels>);

  const handleAddPanel = (panelDefId: string) => {
    const def = panelRegistry.get(panelDefId);
    if (!def) return;

    const defaultConfig = getDefaultConfiguration(def.configurationSchema);

    const sizeMap = {
      small: { w: 3, h: 6 },
      medium: { w: 6, h: 9 },
      large: { w: 9, h: 12 },
      xlarge: { w: 12, h: 16 }
    };

    const dims = sizeMap[def.defaultSize] || sizeMap.medium;

    // Explicitly do NOT set `i` here, rely on the store generation to set `panelInstanceId` and map it to `i`
    const layout = {
      i: 'temp-placeholder',
      x: 0,
      y: Infinity,
      w: dims.w,
      h: dims.h
    };

    addPanelToWorkspace(workspaceId, panelDefId, defaultConfig, layout);
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[600px] max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Add Panel</DialogTitle>
        </DialogHeader>

        <div className="py-2">
          <Input
            placeholder="Search panels..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="flex-1 overflow-y-auto pr-2">
          {Object.keys(groupedPanels).length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">No panels found.</div>
          ) : (
            Object.entries(groupedPanels).map(([category, panels]) => (
              <div key={category} className="mb-6">
                <h3 className="font-semibold capitalize mb-3 text-sm text-muted-foreground border-b pb-1">
                  {category}
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {panels.map(panel => (
                    <div
                      key={panel.id}
                      className="border rounded-md p-3 hover:border-primary cursor-pointer transition-colors flex flex-col"
                      onClick={() => handleAddPanel(panel.id)}
                    >
                      <h4 className="font-medium text-sm">{panel.title}</h4>
                      <p className="text-xs text-muted-foreground mt-1 flex-1">{panel.description}</p>
                      <Button variant="secondary" size="sm" className="w-full mt-3 h-7">Add</Button>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};
