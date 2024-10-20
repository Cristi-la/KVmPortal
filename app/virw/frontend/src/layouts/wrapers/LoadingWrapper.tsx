
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

export default function Loading() {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full border-4 border-gray-300 border-t-gray-900 h-12 w-12" />
          <p className="text-gray-500 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    )
  }


interface LoaderWrapperProps {
    loading: boolean;
    children: React.ReactNode;
  }
  
export const LoadingWrapper: React.FC<LoaderWrapperProps> = ({ loading, children }) => {

    if (!loading)
        return <>{children}</>
    
    return (
        <div className='relative'>
            <div className="absolute flex h-screen w-full items-center justify-center z-50 bg-gray-900/60 backdrop-blur-sm dark:bg-gray-950/60">
                <div className="flex flex-col items-center space-y-4">
                <div className="animate-spin rounded-full border-4 border-secondary border-t-primary h-12 w-12" />
                <p className="text-secondary select-none">Loading...</p>
                </div>
            </div>
            {children}
        </div>
    )
};


