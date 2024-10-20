import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { useContext } from 'react'
import AuthContext from 'context/AuthContext'
import {cn} from '@/lib/utils'


import React, { forwardRef } from 'react';

const ProfileBtn = React.forwardRef<HTMLDivElement,React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => {
  const { user, logout } = useContext(AuthContext)!;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='ghost' className={cn('relative h-10 w-10 rounded-full', className)} >
          <Avatar className='h-10 w-10 border-2 border-secondary'>
            <AvatarImage src={`https://api.dicebear.com/9.x/pixel-art/svg?seed=${user?.username}`} alt='user-ico' className='border border-secondary' />
            <AvatarFallback>SN</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className='w-56' align='start'>
        <DropdownMenuLabel className='font-normal'>
          <div className='flex flex-col space-y-1'>
            <p className='text-sm font-medium leading-none'>{user?.username}</p>
            <p className='text-xs leading-none text-muted-foreground'>
              {user?.email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>
            Profile
            <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem>
            Billing
            <DropdownMenuShortcut>⌘B</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem>New Team</DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => logout()}>
          Log out
          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
});

export default ProfileBtn;
