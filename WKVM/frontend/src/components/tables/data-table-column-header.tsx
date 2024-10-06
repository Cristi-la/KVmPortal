import React from 'react';
import { Button } from '@/components/ui/button'; // Adjust the import path
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
  DropdownMenuCheckboxItem,
} from '@/components/ui/dropdown-menu'; // Adjust the import path
import { Column, Row } from '@tanstack/react-table'; // Adjust the import path
import { PlusCircledIcon, ArrowUpIcon, ArrowDownIcon, CaretSortIcon, MinusIcon, EyeNoneIcon, ZoomInIcon } from '@radix-ui/react-icons'; // Adjust the import path
import { DebouncedInput } from 'components/fields/DebouncedInput'; // Adjust the import path

import { Badge } from '@/components/ui/badge'

import { Separator } from '@/components/ui/separator'
import { useState, useEffect, useCallback } from 'react';


interface DataTableColumnHeaderProps<TData, TValue>
  extends React.HTMLAttributes<HTMLDivElement> {
  column: Column<TData, TValue>;
  title: string;
  sort?: boolean;
  filter?: boolean;
  hide?: boolean;
}

interface SortingMenuItemProps {
  condition: boolean;
  onClick: () => void;
  icon: React.ElementType;
  label: string;
}

const SortingMenuItem: React.FC<SortingMenuItemProps> = ({
  condition,
  onClick,
  icon: Icon,
  label,
}) => {
  if (!condition) return null;

  return (
    <DropdownMenuItem onClick={onClick}>
      <Icon className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
      {label}
    </DropdownMenuItem>
  );
};

export function ColumnHeader<TData, TValue>({
  column,
  title,
  sort = true,
  filter = true,
  hide = true,
}: DataTableColumnHeaderProps<TData, TValue>) {

  return (
    <div className={`flex items-center space-x-2 `} >
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            className="-ml-3 h-8 data-[state=open]:bg-accent"
          >
            <span>{title}</span>
              {(sort) ? (
                (column.getIsSorted() === 'desc') ? (
                  <ArrowDownIcon className="ml-2 h-4 w-4" />
                ) : column.getIsSorted() === 'asc' ? (
                  <ArrowUpIcon className="ml-2 h-4 w-4" />
                ) : (
                  <CaretSortIcon className="ml-2 h-4 w-4" />
                )
              ) : null}
              
            {(filter && column.getFilterValue()) ? (
              <ZoomInIcon className="ml-2 h-4 w-4 z-10" />
            ) : null}
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="start">
          {/* Sorting Options */}
          {sort && (
            <>
              <SortingMenuItem
                condition={column.getIsSorted() !== 'asc'}
                onClick={() => column.toggleSorting(false)}
                icon={ArrowUpIcon}
                label="Sort Ascending"
              />

              <SortingMenuItem
                condition={
                  column.getIsSorted() === 'asc' || column.getIsSorted() === 'desc'
                }
                onClick={() => column.clearSorting()}
                icon={MinusIcon}
                label="Clear Sorting"
              />

              <SortingMenuItem
                condition={column.getIsSorted() !== 'desc'}
                onClick={() => column.toggleSorting(true)}
                icon={ArrowDownIcon}
                label="Sort Descending"
              />
            </>
          )}

          {/* Hiding Option */}
          {hide && column.getCanHide() && (
            <>
              { sort ? <DropdownMenuSeparator /> : null }
              <DropdownMenuItem onClick={() => column.toggleVisibility(false)}>
                <EyeNoneIcon className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
                Hide Column
              </DropdownMenuItem>
            </>
          )}

          {/* Filtering Option */}
          {filter && (
            <>
              { sort || hide ? <DropdownMenuSeparator /> : null }
              <DropdownMenuLabel asChild>
                <DebouncedInput
                  placeholder={`Filter ${title}`}
                  value={(column.getFilterValue() as string) ?? ''}
                  onDebounceChange={(value: string) => {
                    column.setFilterValue(value);
                  }}
                  debounceTime={300}
                  className="h-8 w-[150px] lg:w-[250px] font-normal"
                />
              </DropdownMenuLabel>
            </>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}