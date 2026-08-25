
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppLayout } from '@/layouts/AppLayout';
import { EmptyState } from '@/components/states/EmptyState';
import { useHealthCheck } from '@/hooks/useHealthCheck';

function WelcomePage() {
  const { data, isLoading, error } = useHealthCheck();

  if (isLoading) {
    return <div className="p-4 text-muted-foreground">Checking backend connectivity...</div>;
  }

  if (error) {
    return <div className="p-4 text-destructive">Error connecting to backend: {error.message}</div>;
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8">
      <h2 className="text-2xl font-bold mb-2">Welcome to Financial Terminal</h2>
      <p className="text-muted-foreground mb-6">Phase 8 Shell successfully loaded.</p>
      {data && (
        <div className="bg-muted p-4 rounded-md text-sm">
          <p>Backend Status: <span className="font-bold text-green-500">{data.status}</span></p>
          <p>Database: {data.database}</p>
          <p>Redis: {data.redis}</p>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<WelcomePage />} />
          <Route path="watchlists" element={<EmptyState title="Watchlists" description="Watchlist module coming soon." />} />
          <Route path="news" element={<EmptyState title="News" description="News module coming soon." />} />
          <Route path="screener" element={<EmptyState title="Screener" description="Screener module coming soon." />} />
          <Route path="portfolio" element={<EmptyState title="Portfolio" description="Portfolio module coming soon." />} />
          <Route path="ai" element={<EmptyState title="AI Terminal" description="AI module coming soon." />} />
          <Route path="*" element={<EmptyState title="404" description="Page not found." />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
