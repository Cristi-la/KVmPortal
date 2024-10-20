"use client"

import * as React from "react"
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
} from "@tanstack/react-table"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import useLocalStorage from 'hooks/use-local-storage';
import { DataTableToolbar } from './data-table-toolbar';
import { DataTablePagination } from './data-table-pagination';
import type { CancelablePromise } from '@/api/core/CancelablePromise';
import { useEffect, useMemo, useRef, useCallback, useState  } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import type { DataTableFacetedFilterProps } from './data-table-faceted-filter';

interface DataTableProps<TData, TValue>{
  columns: ColumnDef<TData>[] | any[];
  query: (...any: any) => CancelablePromise<TData | any>; 
  tableKey: string;
  faceFilters?: Array<DataTableFacetedFilterProps<TData, TValue>>;
}

export function DataTable<TData, TValue>({
  columns,
  query,
  faceFilters,
  tableKey = 'default',
}: DataTableProps<TData, TValue>) {
  const uniqueKeyPrefix = `datatable_${tableKey }_`;
  const [globalFilter, setGlobalFilter] = useState('')
  const [rowCount, setRowCount] = useState(0);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [rowSelection, setRowSelection] = React.useState({})
  const [expanded, setExpanded] = useState<ExpandedState>({});
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [sorting, setSorting] = useLocalStorage<SortingState>({
    key: uniqueKeyPrefix + 'sorting',
    defaultValue: [],
  });
  const [pagination, setPagination] = useState<PaginationState>({
      pageIndex: 0, 
      pageSize: 10,
  });
  const [columnVisibility, setColumnVisibility] = useLocalStorage<VisibilityState>({
    key: uniqueKeyPrefix + 'columnVisibility',
    defaultValue:  columns.reduce((acc, column) => {
      if (column.accessorKey && column.meta?.show) {
        acc[column.accessorKey as string] = true;
      }
      return acc;
    }, {} as VisibilityState), 
  });

  const tableColumns = useMemo(() =>
      loading
        ? columns.map((column) => ({
            ...column,
            cell: <Skeleton className="h-4 my-1" />,
          }))
        : columns,
    [loading, columns]
  );
  const tableData = useMemo(
    () => (loading ? Array(10).fill({}) : data),
    [loading, data]
  ); 


  const filters = useMemo(() => {
  return Object.fromEntries(
    columnFilters.filter((f) => f.value).map((f) => [f.id, f.value])
  );
}, [columnFilters]);

  const ordering = useMemo(() => {
    return sorting.length > 0
      ? sorting.map((sort) => `${sort.desc ? '-' : ''}${sort.id}`).join(',')
      : 'id';
  }, [sorting]);


  const [fields, setFields] = React.useState<string>(() => {
    return Object.entries(columnVisibility)
      .filter(([key, value]) => value)
      .map(([key]) => key)
      .join(',');
  });
  const prevFieldsRef = useRef(fields);

  const refreshData = useCallback(async (fieldsOverride?: string) => {
    try {
      // setLoading(true);
      const params = {
        page: pagination.pageIndex,
        pageSize: pagination.pageSize,
        ordering: ordering,
        fields: fieldsOverride || fields,
        search: globalFilter,
        ...filters,
      };
      
      const data = await query(params);
      setData(data.results);
      setRowCount(data.count);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }, [pagination.pageIndex, pagination.pageSize, ordering, fields, globalFilter, filters, query]);


  // USE EFFECTS
  // /---------------------------
  useEffect(() => {
    refreshData();
  }, [globalFilter, filters, ordering, pagination]);

  useEffect(() => {
    const newFields = Object.entries(columnVisibility)
      .filter(([key, value]) => value)
      .map(([key]) => key)
      .join(',');

      if (newFields.length > prevFieldsRef.current.length) refreshData(newFields);

    setFields(newFields);
    prevFieldsRef.current = newFields;
  }, [columnVisibility]);

  // USE EFFECTS
  // /---------------------------

  const table = useReactTable({
      data: tableData,
      columns: tableColumns,
      onColumnVisibilityChange: setColumnVisibility,
      getFacetedRowModel: getFacetedRowModel(),
      debugTable: true,
      
      state: {
          sorting,
          columnFilters,
          columnVisibility,
          rowSelection,
          pagination,
          globalFilter,
          expanded,
      },

      // selection
      getRowId: row => row.id,
      onRowSelectionChange: setRowSelection,

      // expansion
      getExpandedRowModel: getExpandedRowModel(),
      onExpandedChange: setExpanded,

      // main
      getCoreRowModel: getCoreRowModel(),

      // server pagination
      onPaginationChange: setPagination,
      rowCount: rowCount,
      manualPagination: true,

      // server filtering
      manualFiltering: true,
      onColumnFiltersChange: setColumnFilters,
      onGlobalFilterChange: setGlobalFilter,

      // server sorting
      onSortingChange: setSorting,
      manualSorting: true,
  })


  return (
    <div className="space-y-4">
      <DataTableToolbar table={table} filters={faceFilters}/>
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
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                  {/* Render expanded content if the row is expanded */}
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
      <DataTablePagination table={table} />
    </div>
  );
}
