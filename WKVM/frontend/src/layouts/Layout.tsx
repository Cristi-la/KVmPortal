import React from 'react';
import { cn } from '@/lib/utils'

const LayoutContext = React.createContext<{
  offset: number
  fixed: boolean
  base: boolean
} | null>(null)

interface LayoutProps extends React.HTMLAttributes<HTMLDivElement> {
  fixed?: boolean
  base?: boolean
  offset?: number
}


const Layout = ({ className, fixed = false, base = false, ...props }: LayoutProps) => {
  const divRef = React.useRef<HTMLDivElement>(null)
  const [offset, setOffset] = React.useState(0)

  const handleScroll = () => {
    if (divRef.current) {
      setOffset(divRef.current.getBoundingClientRect().top)
    }
  }

  React.useEffect(() => {
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  
  return (
    <LayoutContext.Provider value={{ offset, fixed, base, }}>
      <div
        ref={divRef}
        data-layout={Layout.displayName}
        className={cn(
          'h-full overflow-auto',
          fixed && 'flex flex-col',
          className
        )}
        {...props }
      />
    </LayoutContext.Provider>
  )
}

Layout.displayName = 'Layout'


const Body = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  const { fixed, base } = React.useContext(LayoutContext)!;

  return (
    <div
      ref={ref}
      data-layout={Body.displayName}
      className={cn(
        'px-4 py-4 md:overflow-hidden md:px-8',
        fixed && 'flex-1',
        base && 'bg-scondary dark:bg-secondary/20',
        className
      )}
      {...props}
    />
  )
})


interface LayoutComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  type: 'header' | 'footer',
  sticky?: boolean,
}

const LayoutComponent = React.forwardRef<HTMLDivElement, LayoutComponentProps>(
  ({ className, sticky, type, ...props }, ref) => {
    const { offset, fixed } = React.useContext(LayoutContext)!;
   
    return (
      <div
        ref={ref}
        data-layout={type}
        className={cn(
          `z-10 flex h-[var(--${type}-height)] items-center gap-4 bg-background p-4 md:px-8`,
          offset > 10 && sticky ? 'shadow' : 'shadow-none',
          fixed && 'flex-none',
          sticky && `sticky ${type === 'header' ? 'top-0' : 'bottom-0'}`,
          className
        )}
        {...props}
      />
    );
  }
);

LayoutComponent.displayName = 'LayoutComponent';

const Header = React.forwardRef<HTMLDivElement, Omit<LayoutComponentProps, 'type'>>(
  (props, ref) => <LayoutComponent ref={ref} type="header" {...props} />
);

const Footer = React.forwardRef<HTMLDivElement, Omit<LayoutComponentProps, 'type'>>(
  (props, ref) => <LayoutComponent ref={ref} type="footer" {...props} />
);

function BaseFooter() {
  return (
    <Footer>
      <p className='w-full text-center text-sm text-foreground/40'>
          &copy; Krzysztof Stefański - 2024 - All rights reserved
      </p>
    </Footer>
  );
}

Body.displayName = 'Body';
Header.displayName = 'Header';
Footer.displayName = 'Footer';
BaseFooter.displayName = 'Footer';

Layout.Header = Header
Layout.Body = Body
Layout.Footer = Footer
Layout.BaseFooter = BaseFooter;

export { Layout }

