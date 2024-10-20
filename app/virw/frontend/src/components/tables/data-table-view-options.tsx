import { SlidersHorizontal, Download, Ghost   } from 'lucide-react'
import { Table } from '@tanstack/react-table'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'

interface DataTableViewOptionsProps<TData> {
  table: Table<TData>
}

export function DataTableViewOptions<TData>({
  table,
}: DataTableViewOptionsProps<TData>) {
  return (
    <>
     <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant='outline'
            size='sm'
            className='ml-auto h-8 lg:flex mr-2'
          >
            <Download className='mr-2 h-4 w-4' />
            Export
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align='end' className='w-[150px]'>
          <DropdownMenuLabel>Export as</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem asChild><Button size='sm' variant='outline' className='my-1 w-full cursor-pointer'>JSON</Button></DropdownMenuItem>
          <DropdownMenuItem asChild><Button size='sm' variant='outline' className='my-1 w-full cursor-pointer'>EXCEL</Button></DropdownMenuItem>
          <DropdownMenuItem asChild><Button size='sm' variant='outline' className='w-full cursor-pointer'>CSV</Button></DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant='outline'
            size='sm'
            className='ml-auto h-8 lg:flex'
          >
            <SlidersHorizontal className='mr-2 h-4 w-4' />
            View
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align='end' className='w-[150px]'>
          <DropdownMenuLabel>Toggle columns</DropdownMenuLabel>
          <DropdownMenuSeparator />
          {table
            .getAllColumns()
            .filter(
              (column) =>
                typeof column.accessorFn !== 'undefined' && column.getCanHide()
            )
            .map((column) => {
              return (
                <DropdownMenuCheckboxItem
                  key={column.id}
                  className='capitalize'
                  checked={column.getIsVisible()}
                  onClick={(event) => {
                    event.preventDefault(); // Prevent default closing behavior
                    column.toggleVisibility(!column.getIsVisible()); // Toggle column visibility
                  }}
                >
                  {column.id}
                </DropdownMenuCheckboxItem>
              )
            })}
        </DropdownMenuContent>
      </DropdownMenu>
    </>
  )
}
