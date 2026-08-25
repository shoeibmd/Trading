
import { Search, Settings, User } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';

export function TopBar() {
  const toggleTheme = useAppStore(state => state.toggleTheme);
  const theme = useAppStore(state => state.theme);

  return (
    <header className="flex items-center justify-between h-14 px-4 border-b bg-background shrink-0">
      <div className="flex items-center space-x-4">
        <h1 className="text-xl font-bold tracking-tight text-primary">TERMINAL</h1>
      </div>

      <div className="flex-1 max-w-md mx-4">
        <div className="relative">
          <Search className="absolute left-2.5 top-2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search symbols or news..."
            className="w-full h-8 pl-9 pr-4 rounded-md bg-muted text-sm border-none focus:outline-none focus:ring-1 focus:ring-ring"
            disabled
          />
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-muted text-muted-foreground transition-colors"
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
          <Settings className="h-5 w-5" />
        </button>
        <button className="p-2 rounded-full hover:bg-muted text-muted-foreground transition-colors">
          <User className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}
