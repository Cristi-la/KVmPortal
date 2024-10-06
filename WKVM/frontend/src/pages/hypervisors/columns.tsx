import type { ColumnDef, RowData, Row} from "@tanstack/react-table";
import { Hypervisor } from "@/api/types.gen";
import { ColumnHeader } from 'components/tables/data-table-column-header';
import { ColumnCellTags } from 'components/tables/data-table-column-cell';
import { Checkbox } from "@/components/ui/checkbox"
import { Link } from 'react-router-dom';
import {
  ChevronDownIcon,
  ChevronRightIcon
} from '@radix-ui/react-icons'
import type { FacetedFilterProps } from '/components/tables/data-table-faceted-filter';
import { ApiService } from "@/api/services.gen";
import type { VMAbstract } from "@/api/types.gen";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

declare module '@tanstack/react-table' {
  interface ColumnMeta<TData extends RowData, TValue> {
    show?: boolean,
    expandedContent?: (row: Row<any>) => JSX.Element,
  }
}

export const faceFilers: Array<FacetedFilterProps<any, any>> = [
  {
    id: 'tags',
    title: 'Tags',
    query: ApiService.apiTagList,
  },
]

export const hypervisorColumns: ColumnDef<Hypervisor>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
        className="align-middle"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
        className="align-middle"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "id",
    header: ({column}) => <ColumnHeader column={column} title='id' />,
  },
  {
    accessorKey: "hostname",
    header: ({column}) => <ColumnHeader column={column} title='hostname' />,
    cell: ({getValue, row}) => (<Link className="font-medium text-primary" to={`/hypervisor/${row.id}`}>{getValue() as string}</Link>),
    meta: { show: true },
  },
  {
    accessorKey: "mgt_ip",
    header: ({column}) => <ColumnHeader column={column} title='mgt_ip' />,
    meta: { show: true },
  },
  {
    accessorKey: "tags",
    header: ({column}) => <ColumnHeader title="Tags" column={column} filter={false} sort={false}/>,
    cell: ({row}) => <ColumnCellTags tags={row.original.tags} />,
    meta: { 
      show: true,
    },
  },
  {
    accessorKey: "created",
    header: ({column}) => <ColumnHeader column={column} title='created'  filter={false}/>,
    meta: { show: true },
  },
  {
    id: 'expander',
    header: () => null,
    cell: ({ row }) => (
      <button onClick={() => row.toggleExpanded()} className="flex items-center">
        {row.getIsExpanded() ? (
          <ChevronDownIcon className="h-5 w-5" />
        ) : (
          <ChevronRightIcon className="h-5 w-5" />
        )}
      </button>
    ),
    meta: {
      expandedContent: (row) => (
        <Table >
        <TableCaption className="text-sm">A list of virtual machines on <span className="font-semibold">{row.original.hostname}</span></TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Memory</TableHead>
            <TableHead>vCPU</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
            {row.original.vms.map((vm: VMAbstract) => (
              <TableRow key={vm.id}>
                <TableCell>
                    <Link className="font-medium text-primary/80" to={`/vm/${vm.id}`}>
                      {vm.name}
                    </Link>
                </TableCell>
                <TableCell>{vm.memory}</TableCell>
                <TableCell>{vm.vcpu}</TableCell>
              </TableRow>
            ))}
        </TableBody>
      </Table>
      ),
    }
  },
];