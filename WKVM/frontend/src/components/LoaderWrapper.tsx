
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

interface LoaderWrapperProps {
    loading: boolean;
    children: React.ReactNode;
    className?: string;
  }
  
export const LoaderWrapper: React.FC<LoaderWrapperProps> = ({ loading, children, className }) => {
return loading ? <Skeleton className={cn('w-full h-96', className)}></Skeleton> : <>{children}</>;
};