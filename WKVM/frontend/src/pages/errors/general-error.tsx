import ErrorLayout from 'layouts/ErrorLayout'

export default function GeneralError() {
  return (
    <div>
      <ErrorLayout 
        code={500}
        msg="Oops! Something went wrong :')" 
        description={
          <>
          We apologize for the inconvenience. <br />
          Please try again later.
          </>
        }
      />
    </div>
  );
}
