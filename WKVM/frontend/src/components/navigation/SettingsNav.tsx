import { Settings } from "lucide-react";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
    DropdownMenuGroup,
    DropdownMenuShortcut,
} from "@/components/ui/dropdown-menu"
  
interface SettingsNavProps extends React.HTMLAttributes<HTMLDivElement> {
    isCollapsed: boolean
}

export default function SettingsNav({
    isCollapsed,
}: SettingsNavProps) {
    return (
        <div className={`flex items-center hover:bg-accent px-3 py-2 rounded-md hover:text-accent-foreground ${!isCollapsed ? 'gap-2' : ''}`}>
            <Settings size={20} />
            <div
                className={`flex flex-col justify-end truncate ${isCollapsed ? 'invisible w-0' : 'visible w-auto'}`}
            >
                <span className='font-medium text-warning-foreground'>Admin Panel</span>
            </div>
        </div>
    )
} 