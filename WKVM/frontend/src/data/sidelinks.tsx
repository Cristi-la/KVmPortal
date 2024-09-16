import {
    House ,
    ChartArea ,
    Cable,
    Computer,
    Server,
    Database,
    Cpu,
    Cloud,
    Settings,
    Laptop,
    Monitor,
    Binary,
    Terminal,
    CirclePlus,
    GitPullRequestArrow,
    GitPullRequestCreateArrow,
    NotepadTextDashed,
} from 'lucide-react'

export interface NavLink {
    title: string
    label?: string
    href: string
    icon: JSX.Element
}

  export interface SideLink extends NavLink {
    sub?: NavLink[]
  }
  
export const sidelinks: SideLink[] = [
    {
        title: 'Home',
        label: '',
        href: '/',
        icon: <House  size={20}/>,
    },
    {
        title: 'Hypervisors',
        label: '',
        href: '',
        icon: <Monitor  size={20} />,
        sub: [
            {
                title: 'Database',
                label: '',
                href: '/hypervisor/db',
                icon: <Database size={18} strokeWidth={1} />,
            },
            {
                title: 'Provisioning',
                label: 'test',
                href: '/hypervisor/provision',
                icon: <GitPullRequestArrow size={18} strokeWidth={1} />,
            },
        ],
    },
    {
        title: 'VMs',
        label: '',
        href: '',
        icon: <Cloud  size={22} />,
        sub: [
            {
                title: 'Database',
                label: '',
                href: '/vm/db',
                icon: <Database size={16} strokeWidth={1} />,
            },
            {
                title: 'Create',
                label: '',
                href: '/vm/create',
                icon: <GitPullRequestCreateArrow size={16} strokeWidth={1} />,
            },
            {
                title: 'Templates',
                label: '',
                href: '/vm/templates',
                icon: <NotepadTextDashed size={16} strokeWidth={1} />,
            },
        ],
    },
    {
        title: 'Dashboards',
        label: '',
        href: '/chart',
        icon: <ChartArea  size={20}/>,
    },
    {
        title: 'Termianls',
        label: 'NEW',
        href: '/terminals',
        icon: <Terminal size={18} />,
    },
]
  