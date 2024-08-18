import { Button } from '@/components/ui/button'
import ErrorLayout from 'layouts/ErrorLayout'

export default function MaintenanceError() {
  return (
    <div>
      <ErrorLayout 
        code={503} 
        msg="Website is under maintenance!" 
        description={
          <>
          The site is not available at the moment. <br />
          We'll be back online shortly.
          </>
        }
        buttons={
          <Button variant='outline'>Learn more</Button>
        }
      />
    </div>
  );
}
