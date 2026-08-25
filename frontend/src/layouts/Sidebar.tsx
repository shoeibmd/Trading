
import { NavLink } from 'react-router-dom';
import { LineChart, List, Newspaper, ScanSearch, Briefcase, BrainCircuit } from 'lucide-react';
import { cn } from '@/lib/utils';

export function Sidebar() {
  const links = [
    { to: "/", icon: LineChart, label: "Markets" },
    { to: "/watchlists", icon: List, label: "Watchlists" },
    { to: "/news", icon: Newspaper, label: "News" },
    { to: "/screener", icon: ScanSearch, label: "Screener" },
    { to: "/portfolio", icon: Briefcase, label: "Portfolio" },
    { to: "/ai", icon: BrainCircuit, label: "AI Terminal" },
  ];

  return (
    <aside className="w-16 lg:w-64 border-r bg-muted/30 flex flex-col items-center lg:items-stretch py-4 transition-all shrink-0">
      <nav className="flex-1 space-y-2 px-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => cn(
              "flex items-center space-x-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
              isActive
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            )}
          >
            <link.icon className="h-5 w-5 shrink-0" />
            <span className="hidden lg:inline">{link.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
