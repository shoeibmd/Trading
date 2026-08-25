import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '../../ui/button';

interface PanelErrorProps {
  message?: string;
  onRetry?: () => void;
}

export const PanelError: React.FC<PanelErrorProps> = ({ message = 'Failed to load panel', onRetry }) => {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-4 text-center text-destructive" data-testid="panel-error">
      <AlertCircle className="h-10 w-10 mb-4 opacity-80" />
      <h3 className="font-semibold text-lg mb-2">Panel Error</h3>
      <p className="text-sm opacity-80 mb-6 max-w-xs">{message}</p>
      {onRetry && (
        <Button variant="outline" size="sm" onClick={onRetry} className="gap-2">
          <RefreshCw className="h-4 w-4" />
          Retry
        </Button>
      )}
    </div>
  );
};
