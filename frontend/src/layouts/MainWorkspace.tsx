import React, { useState, useEffect } from 'react';
import { EmptyState } from '../components/states/EmptyState';
import { Plus } from 'lucide-react';
import { Button } from '../components/ui/button';
import { GridLayout } from '../components/workspace/GridLayout';
import { PanelPicker } from '../components/workspace/PanelPicker';
import { useWorkspaceStore } from '../store/useWorkspaceStore';

export const MainWorkspace: React.FC = () => {
  const { workspaces, activeWorkspaceId, loadWorkspaces, isLoading, error } = useWorkspaceStore();
  const [isPanelPickerOpen, setIsPanelPickerOpen] = useState(false);

  useEffect(() => {
    loadWorkspaces();
  }, [loadWorkspaces]);

  const activeWorkspace = workspaces.find(w => w.id === activeWorkspaceId);
  const panelsCount = activeWorkspace?.layout?.panels?.length || 0;

  if (isLoading) {
    return (
      <div className="flex-1 bg-muted/20 relative overflow-hidden flex flex-col h-full items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        <p className="mt-4 text-sm text-muted-foreground">Loading workspaces...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 bg-muted/20 relative overflow-hidden flex flex-col h-full items-center justify-center text-destructive">
        <p>Failed to load workspace data: {error}</p>
        <Button className="mt-4" onClick={() => loadWorkspaces()}>Retry</Button>
      </div>
    );
  }

  if (!activeWorkspace) {
    return (
      <div className="flex-1 bg-muted/20 relative overflow-hidden flex flex-col h-full items-center justify-center">
        <EmptyState
          title="No Active Workspace"
          description="Create or select a workspace to continue"
        />
      </div>
    );
  }

  return (
    <div className="flex-1 bg-muted/20 relative overflow-hidden flex flex-col h-full" data-testid="main-workspace">
      {/* Workspace Toolbar */}
      <div className="h-10 border-b flex items-center justify-between px-4 bg-background">
        <h2 className="text-sm font-semibold">{activeWorkspace.name}</h2>
        <div className="flex items-center gap-2">
          <Button size="sm" onClick={() => setIsPanelPickerOpen(true)} className="h-7 text-xs gap-1">
            <Plus className="h-3.5 w-3.5" />
            Add Panel
          </Button>
        </div>
      </div>

      {/* Workspace Content */}
      <div className="flex-1 overflow-auto relative">
        {panelsCount === 0 ? (
          <EmptyState
            title="Workspace is empty"
            description="Add panels to start building your terminal"
            action={{ label: "Add Panel", onClick: () => setIsPanelPickerOpen(true) }}
          />
        ) : (
          <GridLayout workspaceId={activeWorkspace.id} />
        )}
      </div>

      <PanelPicker
        isOpen={isPanelPickerOpen}
        onClose={() => setIsPanelPickerOpen(false)}
        workspaceId={activeWorkspace.id}
      />
    </div>
  );
};
