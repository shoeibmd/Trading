import React from 'react';
import { Settings, RefreshCw, X, GripHorizontal } from 'lucide-react';
import { Button } from '../ui/button';

interface PanelHeaderProps {
  title: string;
  lastUpdated?: Date;
  onSettingsClick: () => void;
  onRefreshClick: () => void;
  onCloseClick: () => void;
}

export const PanelHeader: React.FC<PanelHeaderProps> = ({
  title,
  lastUpdated,
  onSettingsClick,
  onRefreshClick,
  onCloseClick
}) => {
  return (
    <div className="flex items-center justify-between p-2 border-b bg-muted/40 group">
      <div className="flex items-center gap-2">
        <div className="cursor-move text-muted-foreground opacity-50 hover:opacity-100 transition-opacity">
          <GripHorizontal className="h-4 w-4" />
        </div>
        <h3 className="font-semibold text-sm truncate max-w-[200px]" title={title}>{title}</h3>
      </div>

      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
        {lastUpdated && (
          <span className="text-[10px] text-muted-foreground mr-2">
            {lastUpdated.toLocaleTimeString()}
          </span>
        )}
        <Button variant="ghost" size="icon" className="h-6 w-6 rounded-sm" onClick={onSettingsClick} title="Settings">
          <Settings className="h-3.5 w-3.5" />
        </Button>
        <Button variant="ghost" size="icon" className="h-6 w-6 rounded-sm" onClick={onRefreshClick} title="Refresh">
          <RefreshCw className="h-3.5 w-3.5" />
        </Button>
        <Button variant="ghost" size="icon" className="h-6 w-6 rounded-sm hover:bg-destructive/20 hover:text-destructive" onClick={onCloseClick} title="Close">
          <X className="h-3.5 w-3.5" />
        </Button>
      </div>
    </div>
  );
};
