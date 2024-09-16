import { CircleX } from 'lucide-react'
import { Table } from '@tanstack/react-table'
import { Button } from '@/components/ui/button'
import { DataTableViewOptions } from './data-table-view-options'
import { DebouncedInput } from 'components/customised/DebouncedInput'
import type { DataTableFacetedFilterProps } from './data-table-faceted-filter';
import {DataTableFacetedFilter} from './data-table-faceted-filter'

interface DataTableToolbarProps<TData, TValue> {
  table: Table<TData>,
  filters?: Array<DataTableFacetedFilterProps<TData, TValue>>;
}

export function DataTableToolbar<TData, TValue>({
  table,
  filters,
}: DataTableToolbarProps<TData, TValue>) {
  const isFiltered = table.getState().columnFilters.length > 0

  return (
    <div className='flex'>
      <div className='flex flex-1 gap-y-1 sm:flex-row sm:items-center sm:space-x-2'>
        <DebouncedInput
          placeholder='Global search...'
          value={table.getState().globalFilter}
          onDebounceChange={(value) =>
            table.setGlobalFilter(value)
          }
          className='h-8 w-[150px] lg:w-[250px]'
        />
        <div className='flex gap-x-2'>
          {filters && filters.map((filter) => (
            <DataTableFacetedFilter
              key={filter.id}
              id={filter.id}
              table={table}
              title={filter.title}
              intOptions={filter.intOptions}
              query={filter.query}
            />
          ))}
        </div>
        {(isFiltered || table.getState().globalFilter)  && (
          <Button
            variant='destructive'
            onClick={() => {table.resetColumnFilters(), table.setGlobalFilter('')}}
            className='h-8 lg:flex mr-2'
            size='sm'
          >
            Reset
            <CircleX className='ml-2 h-4 w-4' />
          </Button>
        )}
      </div>
      <DataTableViewOptions table={table} />
    </div>
  )
}
