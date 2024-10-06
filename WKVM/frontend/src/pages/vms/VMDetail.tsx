import { Layout } from 'layouts/Layout'
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

import { ApiService } from '@/api/services.gen';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

export default function VMDetails() {


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
                            <Link to='/vm/db' className='transition-colors hover:text-foreground'>VMs</Link>
                        </BreadcrumbItem>
                        <BreadcrumbSeparator />
                        <BreadcrumbItem>
                            <BreadcrumbPage>Create/Define</BreadcrumbPage>
                        </BreadcrumbItem>
                    </BreadcrumbList>
                </Breadcrumb>
                
            </Layout.Header>

            <Layout.Body className='h-full bg-scondary dark:bg-secondary/20'>
                
            </Layout.Body>

            <Layout.Footer>
                
            </Layout.Footer>
        </Layout>
    );
}
