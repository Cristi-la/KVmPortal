import { useEffect, useState } from 'react'
import { Layout } from 'layouts/Layout'
import { Button } from '@/components/ui/button'
import { 
  FaceIcon,
  DoubleArrowLeftIcon, 
  DoubleArrowRightIcon, 
  HamburgerMenuIcon, 
  Cross1Icon,
} from '@radix-ui/react-icons'
import { Nav, DocLink } from 'components/navigation/Nav'
import { cn } from '@/lib/utils'
import { sidelinks } from 'data/sidelinks'
import SettingsBtn from 'components/navigation/SettingsBtn'
import ProfileBtn from 'components/navigation/ProfileBtn'
import ThemeSwitch from 'components/ThemeSwitch'
import favicon from 'assets/images/favicon.png'
import { Settings, CircleHelp } from "lucide-react";
import { useContext } from 'react'
import AuthContext from 'context/AuthContext'

interface SidebarProps extends React.HTMLAttributes<HTMLElement> {
  isCollapsed: boolean
  setIsCollapsed: React.Dispatch<React.SetStateAction<boolean>>
}

export default function Sidebar({
  className,
  isCollapsed,
  setIsCollapsed,
}: SidebarProps) {
  
  const [navOpened, setNavOpened] = useState(false)
  const { user } = useContext(AuthContext)
  if (!user?.is_staff) return null

  /* Make body not scrollable when navBar is opened */
  useEffect(() => {
    if (navOpened) {
      document.body.classList.add('overflow-hidden')
    } else {
      document.body.classList.remove('overflow-hidden')
    }
  }, [navOpened])

  return (
    <aside
      className={cn(
        `fixed left-0 right-0 top-0 z-50 w-full border-r-2 border-r-muted transition-[width] md:bottom-0 md:right-auto md:h-svh ${isCollapsed ? 'md:w-14' : 'md:w-60'}`,
        className
      )}
    >
      {/* Overlay in mobile */}
      <div
        onClick={() => setNavOpened(false)}
        className={`absolute inset-0 transition-[opacity] delay-100 duration-700 ${navOpened ? 'h-svh opacity-50' : 'h-0 opacity-0'} w-full bg-black md:hidden`}
      />

      <Layout fixed className={navOpened ? 'h-svh' : ''}>
        {/* Header */}
        <Layout.Header
          sticky
          className={`z-50 flex justify-between px-4 py-3 shadow-sm ${!isCollapsed ? 'md:px-4' : 'md:px-1'} `}
        >
          <div className={`flex items-center ${!isCollapsed ? 'gap-2' : ''}`}>
            <img src={favicon} alt="Logo" className='h-11  rounded-lg border border-secondary' />
            <div
              className={`flex flex-col justify-end truncate ${isCollapsed ? 'invisible w-0' : 'visible w-auto'}`}
            >
              <span className='font-bold text-xl text-foreground/70'>VIRW</span>
              <span className='text-xs'>Version 1.0.0</span>
            </div>
          </div>

          {/* Toggle Button in mobile */}
          <div className='md:hidden flex gap-2'>
            <Button
              variant='ghost'
              size='icon'
              aria-label='Toggle Navigation'
              aria-controls='sidebar-menu'
              aria-expanded={navOpened}
              onClick={() => setNavOpened((prev) => !prev)}
            >
              {navOpened ? <Cross1Icon /> : <HamburgerMenuIcon />}
            </Button>
            <ProfileBtn/>
          </div>
          
          
        </Layout.Header>

        {/* Navigation links */}
        
        <Nav
          id='sidebar-menu'
          className={` z-40 h-full flex-1 ${navOpened ? 'max-h-screen' : 'max-h-0 py-0 md:max-h-screen md:py-2'}`}
          closeNav={() => setNavOpened(false)}
          isCollapsed={isCollapsed}
          links={sidelinks}
        />

        <Layout.Footer
          className={`overflow-hidden z-50 justify-between px-4 py-3 shadow-sm md:px-4 items-center hidden md:block`}
        >
          <>
            {/* <div className={`flex flex-col items-center transition-[margin] ${isCollapsed ? 'mb-0' : 'mb-4'}`}>
              <ThemeSwitch />
              <span className={`flex flex-col items-center ${isCollapsed ? 'hidden' : ''}`}>
                <DocLink to='doc'>Documenation</DocLink>
                <DocLink to='help'>Help</DocLink>
              </span>
            </div> */}
            <div className={`flex items-center justify-end gap-2 'flex-col ${isCollapsed ? 'flex-col-reverse' : 'flex-row'}`}>
              <ProfileBtn className={`${!isCollapsed && 'mr-auto'}`} />

              { user.is_staff && <SettingsBtn /> }
              <a href='/help'><CircleHelp /></a>
              <ThemeSwitch />
            </div>
          </>
        </Layout.Footer>

        {/* Scrollbar width toggle button */}
        <Button
          onClick={() => setIsCollapsed((prev) => !prev)}
          size='icon'
          variant='outline'
          className='absolute -right-5 top-1/2 z-50 hidden rounded-full md:inline-flex'
        >
          { isCollapsed ? <DoubleArrowRightIcon height={14} width={14}/> : <DoubleArrowLeftIcon height={14} width={14} /> }
        </Button>
      </Layout>
    </aside>
  )
}
