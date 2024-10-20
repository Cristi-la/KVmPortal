
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

interface SkeletonWrapperProps {
    loading: boolean;
    children: React.ReactNode;
    className?: string;
  }
  
export const SkeletonWrapper: React.FC<SkeletonWrapperProps> = ({ loading, children, className }) => {
return loading ? <Skeleton className={cn('w-full h-96', className)}></Skeleton> : <>{children}</>;
};