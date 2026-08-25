
import { AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ErrorMessageProps {
  message?: string;
  className?: string;
}

export function ErrorMessage({ message = "An error occurred.", className }: ErrorMessageProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center w-full h-full p-6 text-destructive", className)}>
      <AlertCircle size={32} className="mb-2" />
      <p className="text-sm text-center font-medium">{message}</p>
    </div>
  );
}
