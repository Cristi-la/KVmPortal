import * as React from 'react'
import { CheckIcon, PlusCircledIcon } from '@radix-ui/react-icons'
import { Table } from '@tanstack/react-table'

import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Separator } from '@/components/ui/separator'
import type { CancelablePromise } from '@/api/core/CancelablePromise';

export interface DataTableFacetedFilterProps<TData, TValue> {
  id?: string
  title: string
  table?: Table<TData>
  intOptions?: Array<{ id: string; name: string, color?: string }>
  query: (...any: any) => CancelablePromise<TData | any>; 
}

export function DataTableFacetedFilter<TData, TValue>({
  id,
  table,
  title,
  intOptions,
  query,
}: DataTableFacetedFilterProps<TData, TValue>) {
  if (!table) return;

  const column = table.getAllColumns().find((column: { id: string, accessorKey?: string }) => column.id === id || column.accessorKey === id)
  
  if (!column) return;

  const selectedValues = new Set(column?.getFilterValue() as string[])
  const [ options, setOptions ] = React.useState(intOptions || [])

  const refreshTags = React.useCallback(() => {
    if (!query) return;
    query().then((data) => {
      setOptions(data)
    })
  }, [query])

  React.useEffect(() => {refreshTags()}, [refreshTags])
  
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant='outline' size='sm' className='h-8 border-dashed'>
          <PlusCircledIcon className='mr-2 h-4 w-4' />
          {title}
          {selectedValues?.size > 0 && (
            <>
              <Separator orientation='vertical' className='mx-2 h-4' />
              <Badge
                variant='secondary'
                className='rounded-sm px-1 font-normal lg:hidden'
              >
                {selectedValues.size}
              </Badge>
              <div className='hidden space-x-1 lg:flex'>
                {selectedValues.size > 2 ? (
                  <Badge
                    variant='secondary'
                    className='rounded-sm px-1 font-normal'
                  >
                    {selectedValues.size} selected
                  </Badge>
                ) : (
                  options
                    .filter((option) => selectedValues.has(option.id))
                    .map((option) => (
                      <Badge
                        variant='secondary'
                        key={option.id}
                        className='rounded-sm px-1 font-normal'
                      >
                        {option.name}
                      </Badge>
                    ))
                )}
              </div>
            </>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className='w-[150px] p-0 ' align='start'>
        <Command>
          <CommandInput placeholder={title} />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup>
              {options.map((option) => {
                const isSelected = selectedValues.has(option.id)
                return (
                  <CommandItem
                    key={option.id}
                    onSelect={() => {
                      if (isSelected) {
                        selectedValues.delete(option.id)
                      } else {
                        selectedValues.add(option.id)
                      }
                      const filterValues = Array.from(selectedValues)
                      column?.setFilterValue(
                        filterValues.length ? filterValues : undefined
                      )
                    }}
                  >
                    <div
                      className={cn(
                        'mr-2 flex h-4 w-4 items-center justify-center rounded-sm border border-primary',
                        isSelected
                          ? 'bg-primary text-primary-foreground'
                          : 'opacity-50 [&_svg]:invisible'
                      )}
                    >
                      <CheckIcon className={cn('h-4 w-4')} />
                    </div>

                      { (option.color) ? 
                        (<Badge
                          key={option.id}
                          style={{ backgroundColor: option.color }}
                          className="px-1 py-0.5 text-xs text-nowrap"
                        >{option.name}</Badge>)
                        : (<span>{option.name}</span>)
                      }

                  </CommandItem>
                )
              })}
            </CommandGroup>
            {selectedValues.size > 0 && (
              <>
                <CommandSeparator />
                <CommandGroup>
                  <CommandItem
                    onSelect={() => column?.setFilterValue(undefined)}
                    className='justify-center text-center'
                  >
                    Clear filters
                  </CommandItem>
                </CommandGroup>
              </>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
