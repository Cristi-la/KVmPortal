import { Moon, Sun } from 'lucide-react'
<<<<<<< HEAD:app/virw/frontend/src/components/ThemeSwitch.tsx
import { useTheme } from 'layouts/wrapers/ThemeWrapper'
=======
import { useTheme } from 'layouts/ThemeWrapper'
>>>>>>> 5547abb4a7464bf1c092df7da4bda8dcd98808dc:WKVM/frontend/src/components/ThemeSwitch.tsx
import { Button } from '@/components/ui/button'
import { useEffect } from 'react'

export default function ThemeSwitch() {
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    const themeColor = theme === 'dark' ? '#020817' : '#fff'
    const metaThemeColor = document.querySelector("meta[name='theme-color']")
    metaThemeColor && metaThemeColor.setAttribute('content', themeColor)
  }, [theme])

  return (
    <Button
      size='icon'
      variant='ghost'
      className='rounded-full'
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
    >
      {theme === 'light' ? <Moon size={25} /> : <Sun size={25} />}
    </Button>
  )
}
