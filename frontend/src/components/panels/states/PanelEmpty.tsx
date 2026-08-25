import React from 'react';
import { Inbox } from 'lucide-react';

interface PanelEmptyProps {
  message?: string;
}

export const PanelEmpty: React.FC<PanelEmptyProps> = ({ message = 'No data available' }) => {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-4 text-center text-muted-foreground" data-testid="panel-empty">
      <div className="bg-muted p-4 rounded-full mb-4">
        <Inbox className="h-8 w-8 opacity-50" />
      </div>
      <h3 className="font-medium">No Data</h3>
      <p className="text-sm mt-1 max-w-xs">{message}</p>
    </div>
  );
};
