
import { PackageOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

interface EmptyStateProps {
  title?: string;
  description?: string;
  className?: string;
}

export function EmptyState({
  title = "No Data Found",
  description = "There is nothing to display here yet.",
  className
}: EmptyStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center w-full h-full p-8 text-muted-foreground", className)}>
      <PackageOpen size={48} className="mb-4 opacity-50" />
      <h3 className="text-lg font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-center">{description}</p>
    </div>
  );
}
