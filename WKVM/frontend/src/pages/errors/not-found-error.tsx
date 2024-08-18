import ErrorLayout from 'layouts/ErrorLayout'

export default function NotFoundError() {
  return (
    <div>
      <ErrorLayout 
        code={404} 
        msg="Oops! Page Not Found!" 
        description={
          <>
          It seems like the page you're looking for <br />
          does not exist or might have been removed.
          </>
        }
      />
    </div>
  );
}
