import React, { useMemo, useEffect, useRef } from 'react';
import { Responsive, WidthProvider, Layout, Layouts } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { panelRegistry } from '../../services/panelRegistry';
import { PanelContainer } from '../panels/PanelContainer';
import { PanelConfiguration } from '../../types/panel';

const ResponsiveGridLayout = WidthProvider(Responsive);

interface GridLayoutProps {
  workspaceId: string;
}

export const GridLayout: React.FC<GridLayoutProps> = ({ workspaceId }) => {
  const {
    workspaces,
    updatePanelLayouts,
    removePanelFromWorkspace,
    updatePanelConfiguration
  } = useWorkspaceStore();

  const workspace = workspaces.find(w => w.id === workspaceId);
  const panels = workspace?.layout?.panels || [];

  const isMounted = useRef(false);

  useEffect(() => {
    isMounted.current = true;
    return () => { isMounted.current = false; };
  }, []);

  const handleLayoutChange = (currentLayout: Layout[], allLayouts: Layouts) => {
    if (!isMounted.current) return;
    updatePanelLayouts(workspaceId, currentLayout);
  };

  const handleClosePanel = (panelInstanceId: string) => {
    removePanelFromWorkspace(workspaceId, panelInstanceId);
  };

  const handleConfigChange = (panelInstanceId: string, config: PanelConfiguration) => {
    updatePanelConfiguration(workspaceId, panelInstanceId, config);
  };

  const layouts = useMemo(() => {
    const layoutArray: Layout[] = panels.map(p => ({
      i: p.panelInstanceId,
      x: p.layout.x,
      y: p.layout.y,
      w: p.layout.w,
      h: p.layout.h,
      minW: p.layout.minW,
      maxW: p.layout.maxW,
      minH: p.layout.minH,
      maxH: p.layout.maxH
    }));
    return { lg: layoutArray };
  }, [panels]);

  if (panels.length === 0) {
    return null;
  }

  return (
    <ResponsiveGridLayout
      className="layout min-h-full"
      layouts={layouts}
      breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
      cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
      rowHeight={30}
      onLayoutChange={handleLayoutChange}
      isDraggable={true}
      isResizable={true}
      draggableHandle=".cursor-move"
      margin={[16, 16]}
      useCSSTransforms={true}
    >
      {panels.map(panel => {
        const definition = panelRegistry.get(panel.panelDefinitionId);
        if (!definition) return <div key={panel.panelInstanceId}>Panel definition not found</div>;

        return (
          <div key={panel.panelInstanceId} className="h-full w-full">
            <PanelContainer
              panelId={panel.panelInstanceId}
              definition={definition}
              initialConfiguration={panel.configuration}
              onClose={() => handleClosePanel(panel.panelInstanceId)}
              onConfigurationChange={(config) => handleConfigChange(panel.panelInstanceId, config)}
            />
          </div>
        );
      })}
    </ResponsiveGridLayout>
  );
};
