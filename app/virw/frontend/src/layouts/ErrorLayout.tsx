import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import PageTitle from 'utils/page-title';

interface ErrorLayoutProps {
  code: number;
  msg: string;
  description: JSX.Element;
  buttons?: JSX.Element;
}

const ErrorLayout: React.FC<ErrorLayoutProps> = ({ code, msg, description, buttons }) => {
  const navigate = useNavigate();

  return (
    <div className='h-svh'>
      <PageTitle title={`${code} - ${msg}`} />
      <div className='m-auto flex h-full w-full flex-col items-center justify-center gap-2'>
        <h1 className='text-[7rem] font-bold leading-tight'>{code}</h1>
        <span className='font-medium'>{msg}</span>
        <p className='text-center text-muted-foreground'>
          {description}
        </p>
        <div className='mt-6 flex gap-4'>
          {
            buttons ? buttons : 
            <>
              <Button variant='outline' onClick={() => navigate(-1)}>
              Go Back
              </Button>
              <Button onClick={() => navigate('/')}>Back to Home</Button>
            </>
          }
        </div>
      </div>
    </div>
  );
};

export default ErrorLayout;