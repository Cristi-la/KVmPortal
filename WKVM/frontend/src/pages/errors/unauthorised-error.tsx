import ErrorLayout from 'layouts/ErrorLayout'

export default function UnauthorisedError() {
  return (
    <div>
      <ErrorLayout 
        code={401} 
        msg="Oops! You don't have permission to access this page." 
        description={
          <>
          It looks like you tried to access a resource that requires proper authentication. 
          <br />
          Please log in with the appropriate credentials.
          </>
        }
      />
    </div>
  );
}
