import { Layout } from 'layouts/Layout'
import { DataTable } from 'components/tables/data-table'
import { ApiService } from '@/api/services.gen';
import { useMemo } from "react";
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

    console.log(user.profiles[0].name)

    return (
        <Layout fixed>
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
                            <Link to='/hypervisor/db' className='transition-colors hover:text-foreground'>Hypervisors</Link>
                        </BreadcrumbItem>
                        <BreadcrumbSeparator />
                        <BreadcrumbItem>
                            <BreadcrumbPage>Provisioning</BreadcrumbPage>
                        </BreadcrumbItem>
                    </BreadcrumbList>
                </Breadcrumb>
                
            </Layout.Header>

            <Layout.Body>
                
            </Layout.Body>

        </Layout>
    );
}
