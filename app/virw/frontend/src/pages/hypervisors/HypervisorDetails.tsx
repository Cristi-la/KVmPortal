import { Layout } from 'layouts/Layout'
import { DataTable } from 'components/tables/data-table'
import { ApiService } from '@/api/services.gen';
import { useMemo } from "react";
import { useState, useEffect } from 'react';
import AuthContext from 'context/AuthContext';
import { useContext, useCallback } from 'react';
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    BreadcrumbEllipsis,
} from "vendor/components/ui/breadcrumb"
import { useParams, Navigate, Link } from 'react-router-dom';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
import type { Hypervisor, VMAbstract } from '@/api/types.gen';
import { useNavigate } from 'react-router-dom';
import { formatDate as fd } from 'utils/parse';
import type { TagAbstract, XmlAbstract } from '@/api/types.gen';
import { Tag, TagComponent } from 'components/Tag';
import XmlCard from 'components/cards/XmlCard';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import VMTable from 'components/tables/local-vm-table';
import { ScrollArea, ScrollBar  } from "@/components/ui/scroll-area"
import { FieldProvider, Record, Key, Value, SearchField } from 'components/fields/fields-search';
import { SkeletonWrapper } from 'layouts/wrapers/SkeletonWrapper';

export default function HypervisorsList() {
    const { id } = useParams();
    const root = '/hypervisor/';
    const navigation = useNavigate();

    const [ loading, setLoading] = useState(true);
    const [ hypervisor, setHypervisor] = useState<Hypervisor|null>(null);
    const [ tags, setTags ] = useState<TagAbstract[]>([]);
    const [ xmls, setXmls ] = useState<XmlAbstract[]>([]);
    const [ vms, setVMs ] = useState<VMAbstract[]>([]);

    if (!id || isNaN(Number(id))) {
        return <Navigate to={root} />;
    };

    useEffect(() => {
        ApiService.apiHypervisorRetrieve({ id: Number(id) })
          .then((res) => {
            setHypervisor(res);
            setTags(res.tags);
            setXmls(res.xmls);
            setVMs(res.vms);
          })
          .catch((err) => {
            navigation(root, { replace: true });
          }).finally(() => setLoading(false));
    }, [id]);

    return (
        <Layout base>
            <Layout.Header>
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
                        <Link to='/hypervisor' className='transition-colors hover:text-foreground'>Hypervisors</Link>
                    </BreadcrumbItem>
                    <BreadcrumbSeparator />
                    <BreadcrumbItem>
                    <BreadcrumbPage>
                        <LoaderWrapper loading={loading} className='h-60'>
                           {hypervisor?.hostname}
                        </LoaderWrapper>
                    </BreadcrumbPage>
                    </BreadcrumbItem>
                </BreadcrumbList>
                </Breadcrumb>
            </Layout.Header>


            <Layout.Body>
                <LoaderWrapper loading={loading}>
                    <FieldProvider>
                        <div className="flex justify-between lg:flex-row-reverse flex-col gap-1">
                            <ScrollArea className='h-auto'>
                                <div className="flex gap-1 pb-3 align-middle">
                                    <TagComponent tags={tags} />
                                </div>
                                <ScrollBar orientation="horizontal" />
                            </ScrollArea>

                            <div className="relative mb-2 lg:min-w-96 lg:mr-16">
                                <SearchField />
                            </div>
                        </div>

                        <Tabs defaultValue='general' className='mb-8'>
                            <TabsList className="flex flex-row mb-1">
                            
                                <TabsTrigger value='general' className="grow" >
                                    General
                                </TabsTrigger>
                                <TabsTrigger value='capabilities' className="grow" >
                                    Capabilities
                                </TabsTrigger>
                                <TabsTrigger value='vms' className="grow" >
                                    VMs
                                </TabsTrigger>

                            </TabsList>

                            <TabsContent value='general'>
                                <Card className="grow">
                                    <CardContent className="p-3 grid grid-flow-row-dense xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-3">
                                        <Card>
                                            <CardHeader className="bg-primary rounded-t text-primary-foreground text-center p-1">
                                                <CardTitle className='text-md'>Components</CardTitle>
                                            </CardHeader>
                                            <CardContent className='py-2'>
                                                <Record>
                                                    <Key>IP</Key>: <Value>10.0.0.2</Value>
                                                </Record>
                                                <Record>
                                                    <Key>BMC</Key>: <Value>192.168.1.2</Value>
                                                </Record>
                                                <Record>
                                                    <Key>Hostname</Key>: <Value>dns2s1</Value>
                                                </Record>
                                            </CardContent>
                                        </Card>
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value='capabilities'>
                                <Card className="grow">
                                    <CardContent className="p-3">
                                        kkk2
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value='vms'>
                                <Card className="grow">
                                    <CardContent className="p-3">
                                        kkk3
                                    </CardContent>
                                </Card>
                            </TabsContent>

                        </Tabs>
                    </FieldProvider>
                </LoaderWrapper>

                <LoaderWrapper loading={loading}>
                    <VMTable vms={vms} className='mb-3'/>
                </LoaderWrapper>
                
                <LoaderWrapper loading={loading}>
                    <XmlCard types={xmls} get={ApiService.apiHypervisorXmlRetrieve} hypervisor_id={Number(id)} />
                </LoaderWrapper>
            </Layout.Body>
        </Layout>
    );
}


{/* <Card className="grow">
                        <CardHeader>
                            <CardTitle className='flex flex-row justify-between items-center'>
                                <div className='w-auto text-nowrap'>
                                    Hypervisor Overview
                                </div>
                                <div className='flex gap-2 overflow-hidden text-ellipsis ml-2'>
                                    {tags.map((tag: TagAbstract) => (
                                        <Tag key={tag.id} color={tag.color} className=''>
                                            {tag.name}
                                        </Tag>
                                    ))}
                                </div>
                            </CardTitle>
                            <CardDescription>
                                    Information updated at {formatDate(hypervisor?.updated)!}
          
                            </CardDescription>
                        </CardHeader>
                        <CardContent className='flex flex-wrap'>
                            <div>
                                <div className='text-lg font-bold'>Hostname:</div>
                            </div>
                            <div>
                                <div className='text-lg ml-3'>{hypervisor?.hostname}</div>
                            </div>
                        </CardContent>
                    </Card> */}