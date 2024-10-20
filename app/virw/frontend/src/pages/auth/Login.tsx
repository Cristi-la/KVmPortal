import { UserAuthForm } from 'components/user-auth-form'
import bg from 'assets/images/bg.gif'

export default function Login() {
    return (
      <>
      <div className='container relative grid h-svh flex-col items-center justify-center lg:max-w-none lg:grid-cols-2 lg:px-0'>
        <div className='relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex'>
          <div className='absolute inset-0 bg-zinc-900 bg-cover'  style ={ { backgroundImage:`url(${bg})` } } />

            <div className='relative z-20 mt-auto'>
              <blockquote className='space-y-2'>
                  <p className='text-lg'>
                    Virtual Web 1.0.0
                  </p>
                  <footer className='text-sm'>A platform for creating and managing virtual events...</footer>
              </blockquote>
            </div>
          </div>


          <div className='lg:p-8'>
              <div className='mx-auto flex w-full flex-col justify-center space-y-2 sm:w-[350px]'>
                <div className='flex flex-col space-y-2 text-center '>
                    <h1 className='text-4xl font-semibold tracking-tight font-serif'>
                      VIRW
                    </h1>

                    <hr />
                    <hr className="w-56 mx-auto" />

                    <p className='text-sm text-muted-foreground text-center'>
                      Enter your username and password below <br />
                      to log into your account
                    </p>
                </div>
                <UserAuthForm />
                {/* <p className='px-8 text-center text-sm text-muted-foreground'>
                  By clicking login, you agree to our{' '}
                  <a
                    href='/terms'
                    className='underline underline-offset-4 hover:text-primary'
                  >
                    Terms of Service
                  </a>{' '}
                  and{' '}
                  <a
                    href='/privacy'
                    className='underline underline-offset-4 hover:text-primary'
                  >
                    Privacy Policy
                  </a>
                  .
                </p> */}
              </div>
                
          </div>
        </div>
      </>
    )
  }
  