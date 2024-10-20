import React from "react"
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Link } from "react-router-dom"
import type { VMAbstract } from "@/api/types.gen"
import { cn } from "@/lib/utils"
<<<<<<< HEAD:app/virw/frontend/src/components/tables/local-vm-table.tsx
import { formatDate as fd, formatState as fs } from 'utils/parse';
=======
import { formatDate as fd, formatState as fs } from 'utils/data';
>>>>>>> 5547abb4a7464bf1c092df7da4bda8dcd98808dc:WKVM/frontend/src/components/tables/local-vm-table.tsx
import { LocalDataTable } from "components/tables/data-table-local"
import type { ColumnDef } from "@tanstack/react-table";

export interface VMTableProps
  extends React.HTMLAttributes<HTMLDivElement> {
    vms: VMAbstract[];
    }

const columns: ColumnDef<VMAbstract>[] = [
    {
        header: 'Name',
        accessorKey: 'name',
        cell: ({ row }) => (
        <Link className="font-medium text-primary/80" to={`/vm/${row.original.id}`}>
            {row.original.name}
        </Link>
        ),
    },
    {
        header: 'State',
        accessorKey: 'state',
        cell: ({ getValue }) => fs(getValue() as string),
    },
    {
        header: 'vCPU',
        accessorKey: 'vcpu',
    },
    {
        header: 'Memory',
        accessorKey: 'memory',
    },
    {
        header: 'Updated',
        accessorKey: 'updated',
        cell: ({ getValue }) => fd(getValue() as string),
    },
    {
        header: 'Created',
        accessorKey: 'created',
        cell: ({ getValue }) => fd(getValue() as string),
    },
]

const VMTable = React.forwardRef<HTMLDivElement, VMTableProps>(
    ({vms, className, ...props }, ref) => {
      return (
            LocalDataTable<VMAbstract, any>({
                data: vms,
                columns: columns,
                className: className,
                ...props,
            })
        );
    },
  );



VMTable.displayName = 'VMTable';

export default VMTable