import React from 'react';

export function MainWorkspace({ children }: { children: React.ReactNode }) {
  return (
    <main className="flex-1 overflow-hidden bg-background relative flex flex-col">
      {children}
    </main>
  );
}
