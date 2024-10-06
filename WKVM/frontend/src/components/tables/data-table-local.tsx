"use client"

import React, { MouseEvent } from 'react';
import {
    PaginationState,
    ColumnDef,
    ColumnFiltersState,
    SortingState,
    flexRender,
    getCoreRowModel,
    useReactTable,
    VisibilityState,
    getFacetedRowModel,
    getExpandedRowModel,
    ExpandedState,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
} from "@tanstack/react-table"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { DataTablePagination } from './data-table-pagination';
import { useState  } from "react";
import { cn } from "@/lib/utils";
import { copyClipboard } from "utils/data";


interface DataTableProps<TData, TValue>{
  columns: ColumnDef<TData>[] | any[];
  data: TData[];
  props?: any; 
  className?: string; 
}


export function LocalDataTable<TData, TValue>({
  data,
  columns,
  className,
  ...props
}: DataTableProps<TData, TValue>) {
  const [globalFilter, setGlobalFilter] = useState('')
  const [rowSelection, setRowSelection] = React.useState({})
  const [expanded, setExpanded] = useState<ExpandedState>({});
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [pagination, setPagination] = useState<PaginationState>({pageIndex: 0, pageSize: 10,});
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>(()=> {
    return columns.reduce((acc, column) => {
      if (column.accessorKey && column.meta?.show) {
        acc[column.accessorKey as string] = true;
      }
      return acc;
    });
  });

  const table = useReactTable({
      data: data,
      columns: columns,
      state: {
          sorting,
          columnFilters,
          columnVisibility,
          rowSelection,
          pagination,
          globalFilter,
          expanded,
      },
      onSortingChange: setSorting,
      onColumnFiltersChange: setColumnFilters,
      getCoreRowModel: getCoreRowModel(),
      getPaginationRowModel: getPaginationRowModel(),
      getSortedRowModel: getSortedRowModel(),
      getFilteredRowModel: getFilteredRowModel(),
      onColumnVisibilityChange: setColumnVisibility,
      onRowSelectionChange: setRowSelection,
      getExpandedRowModel: getExpandedRowModel(),
      onExpandedChange: setExpanded,
      onPaginationChange: setPagination,
      onGlobalFilterChange: setGlobalFilter,
  })


  return (
    <div className={cn("space-y-2", className)} {...props}>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id} colSpan={header.colSpan}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.length ? (
              table.getRowModel().rows.map((row) => (
                <React.Fragment key={row.id}>
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && 'selected'}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id} onDoubleClick={(e) => copyClipboard(e, cell.getValue() as string)}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                  {row.getIsExpanded() && (
                    <TableRow >
                      <TableCell colSpan={columns.length}>
                        {columns.find(col => col.id === 'expander')?.meta?.expandedContent?.(row)}
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <DataTablePagination table={table} selection={false} />
    </div>
  );
}
