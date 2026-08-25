import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { TopBar } from './TopBar';
import { Sidebar } from './Sidebar';
import { MainWorkspace } from './MainWorkspace';
import { useAppStore } from '@/store/useAppStore';

export function AppLayout() {
  const theme = useAppStore(state => state.theme);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden text-foreground bg-background">
      <TopBar />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <MainWorkspace>
          <Outlet />
        </MainWorkspace>
      </div>
    </div>
  );
}
