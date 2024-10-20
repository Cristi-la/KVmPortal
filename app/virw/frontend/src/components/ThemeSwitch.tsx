import { Moon, Sun } from 'lucide-react'
import { useTheme } from 'layouts/wrapers/ThemeWrapper'
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
