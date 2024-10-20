import { Layout } from 'layouts/Layout'
import { DataTable } from 'components/tables/data-table'
import { ApiService } from '@/api/services.gen';
import { useMemo } from "react";
import { hypervisorColumns, faceFilers} from 'pages/hypervisors/columns';
import AuthContext from 'context/AuthContext';
import { useContext } from 'react';
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    BreadcrumbEllipsis,
} from "vendor/components/ui/breadcrumb"
import { Link } from 'react-router-dom';



export default function HypervisorsList() {
    const { user } = useContext(AuthContext);
    const table = useMemo(()=> <DataTable
        columns={hypervisorColumns}
        tableKey={'hypervizor'}
        query={ApiService.apiHypervisorList}
        faceFilters={faceFilers}
        />,
        [hypervisorColumns])

    return (
        <Layout>
            <Layout.Header sticky>
                <Breadcrumb>
                    <BreadcrumbList>
                        <BreadcrumbItem>
                            <Link to='/' className='transition-colors hover:text-foreground'>Home</Link>
                        </BreadcrumbItem>
                        <BreadcrumbSeparator />
                        <BreadcrumbItem>
                            <BreadcrumbEllipsis className="h-4 w-4" />
                        </BreadcrumbItem>
                        <BreadcrumbSeparator />
                        <BreadcrumbItem>
                            <BreadcrumbPage>Hypervisors</BreadcrumbPage>
                        </BreadcrumbItem>
                    </BreadcrumbList>
                </Breadcrumb>

                {/* <HoverCard>
                    <HoverCardTrigger asChild>
                        <Button variant="link">@nextjs</Button>
                    </HoverCardTrigger>
                    <HoverCardContent className="w-80">
                        <div className="flex justify-between space-x-4">
                        <Avatar>
                            <AvatarImage src="https://github.com/vercel.png" />
                            <AvatarFallback>VC</AvatarFallback>
                        </Avatar>
                        <div className="space-y-1">
                            <h4 className="text-sm font-semibold">@nextjs</h4>
                            <p className="text-sm">
                            The React Framework – created and maintained by @vercel.
                            </p>
                            <div className="flex items-center pt-2">
                            <CalendarIcon className="mr-2 h-4 w-4 opacity-70" />{" "}
                            <span className="text-xs text-muted-foreground">
                                Joined December 2021
                            </span>
                            </div>
                        </div>
                        </div>
                    </HoverCardContent>
                </HoverCard> */}
                
            </Layout.Header>

            <Layout.Body className='h-full bg-scondary dark:bg-secondary/20'>
                {table}
            </Layout.Body>

            <Layout.Footer>
                
            </Layout.Footer>
        </Layout>
    );
}
