import { Outlet } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import useIsCollapsed from '../hooks/use-is-collapsed'


export default function OutLayout() {
  const [isCollapsed, setIsCollapsed] = useIsCollapsed()
  return (
      <div className='relative h-full overflow-hidden bg-background'>
        <Sidebar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />
        <main
          id='content'
          className={`overflow-x-hidden pt-16 transition-[margin] md:overflow-y-hidden md:pt-0 ${isCollapsed ? 'md:ml-14' : 'md:ml-60'} h-full`}
        >
          <Outlet />
        </main>
      </div>
  )
}
