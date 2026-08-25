import React from 'react';
import { Skeleton } from '../../ui/skeleton';

export const PanelLoading: React.FC = () => {
  return (
    <div className="w-full h-full flex flex-col space-y-4 p-4" data-testid="panel-loading">
      <Skeleton className="h-8 w-3/4" />
      <Skeleton className="h-full w-full" />
    </div>
  );
};
