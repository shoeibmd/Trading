import React, { useState } from 'react';
import { Search, Bell, Settings, LayoutDashboard, Menu, Moon, Sun } from 'lucide-react';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import { WorkspaceManager } from '../components/workspace/WorkspaceManager';
import { useAppStore } from '../store/useAppStore';

export const TopBar: React.FC = () => {
  const [isWorkspaceManagerOpen, setIsWorkspaceManagerOpen] = useState(false);
  const { workspaces, activeWorkspaceId, setActiveWorkspace } = useWorkspaceStore();
  const { isDarkMode, toggleTheme } = useAppStore();

  return (
    <>
      <header className="h-14 border-b bg-background flex items-center justify-between px-4 sticky top-0 z-40" data-testid="top-bar">
        {/* Left section */}
        <div className="flex items-center gap-4 w-1/3">
          <div className="md:hidden">
            <Menu className="h-5 w-5 text-muted-foreground cursor-pointer hover:text-foreground transition-colors" />
          </div>
          <div className="hidden md:flex items-center gap-2">
            <div className="bg-primary/10 p-1.5 rounded-md">
              <LayoutDashboard className="h-5 w-5 text-primary" />
            </div>
            <span className="font-bold text-lg tracking-tight">FinTerm</span>
          </div>
        </div>

        {/* Center section - Workspace Selector & Search */}
        <div className="flex-1 max-w-xl flex items-center gap-4">
          {workspaces.length > 0 && (
            <div className="flex items-center gap-2">
              <select
                className="bg-muted text-sm rounded-md px-2 py-1.5 border-none focus:ring-1 focus:ring-primary cursor-pointer w-48 truncate"
                value={activeWorkspaceId || ''}
                onChange={(e) => setActiveWorkspace(e.target.value)}
              >
                {workspaces.map(w => (
                  <option key={w.id} value={w.id}>{w.name}</option>
                ))}
              </select>
              <button
                onClick={() => setIsWorkspaceManagerOpen(true)}
                className="text-xs text-muted-foreground hover:text-primary whitespace-nowrap px-2"
              >
                Manage
              </button>
            </div>
          )}

          <div className="relative w-full hidden sm:block">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search instruments, news, commands..."
              className="w-full bg-muted/50 border-none rounded-md pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary transition-all"
            />
            <div className="absolute right-2 top-2 text-[10px] bg-background border px-1.5 py-0.5 rounded text-muted-foreground font-medium">
              ⌘K
            </div>
          </div>
        </div>

        {/* Right section */}
        <div className="flex items-center justify-end gap-3 w-1/3">
          <button onClick={toggleTheme} className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-full transition-colors" title="Toggle theme">
            {isDarkMode ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          </button>
          <div className="relative">
            <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-full transition-colors" title="Notifications">
              <Bell className="h-4 w-4" />
            </button>
            <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-destructive border-2 border-background"></span>
          </div>
          <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-full transition-colors" title="Settings">
            <Settings className="h-4 w-4" />
          </button>
          <div className="h-8 w-8 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center text-sm font-medium text-primary ml-2 cursor-pointer">
            JD
          </div>
        </div>
      </header>

      <WorkspaceManager
        isOpen={isWorkspaceManagerOpen}
        onClose={() => setIsWorkspaceManagerOpen(false)}
      />
    </>
  );
};
