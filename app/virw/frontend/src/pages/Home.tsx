import {Layout} from 'layouts/Layout'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbEllipsis,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "vendor/components/ui/breadcrumb"
import { toast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"
import { ToastAction } from "@/components/ui/toast"
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

import React, {useContext} from 'react';
import AuthContext from 'context/AuthContext'
import TenantContext from 'context/TenantContext'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  House ,
  ChartArea ,
  Cable,
  Computer,
  Server,
  Database,
  Cpu,
  Cloud,
  Settings,
  Laptop,
  Monitor,
  Binary,
  Terminal,
  CirclePlus,
  GitPullRequestArrow,
  GitPullRequestCreateArrow,
  NotepadTextDashed,
  Download,
  Pen,
  ClipboardList,
  Activity, 
} from 'lucide-react'
import {Badge} from '@/components/ui/badge'

import {VmCreationChart, HypervisorOsChart, VMStatusChart } from './charts'

export default  function Home() {
  const { user, authTokens } = useContext(AuthContext)!;
  const { changeTenat } = useContext(TenantContext)!;

  return (
    <Layout fixed>
      <Layout.Header sticky>
        <Breadcrumb>
          <BreadcrumbList>
              <BreadcrumbItem>
                  Home
              </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </Layout.Header>

      <Layout.Body>
      <div className='mb-2 flex items-center justify-between space-y-2'>
          <h1 className='text-4xl font-bold tracking-tight'>Home</h1>
          <div className='flex items-center space-x-2'>
            <Button variant={'outline'} disabled>
              <Pen size={16} />
            </Button>
            <Button variant={'outline'} disabled>
              <Download size={16}/>
            </Button>
          </div>
        </div>
        <Tabs
          orientation='vertical'
          defaultValue='overview'
          className='space-y-4'
        >
          <div className='w-full overflow-x-auto pb-2'>
            <TabsList>
              <TabsTrigger value='overview'>Overview</TabsTrigger>
              <TabsTrigger value='analytics'>Analytics</TabsTrigger>
              <TabsTrigger value='notifications'>
                Notifications
                <Badge className='ml-1'  variant={'destructive'}>0</Badge>
              </TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value='overview' className='space-y-4'>
            <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>
                    Total Hypervisors
                  </CardTitle>
                  <Monitor size={20} />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>0</div>
                  <p className='text-xs text-muted-foreground'>
                    +0 from last month
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>
                    Totall VMs
                  </CardTitle>
                  <Cloud size={20} />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>0</div>
                  <p className='text-xs text-muted-foreground'>
                    +0 from last month
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>Task Run</CardTitle>
                  <ClipboardList size={20} />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>0</div>
                  <p className='text-xs text-muted-foreground'>
                    +0 since last hour
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium'>
                    VM Mac Addresses
                  </CardTitle>
                  <Activity size={20} />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>0</div>
                  <p className='text-xs text-muted-foreground'>
                    +0 since last hour
                  </p>
                </CardContent>
              </Card>
            </div>
            <div className='grid grid-cols-1 gap-4 lg:grid-cols-7'>
              <Card className='col-span-1 lg:col-span-4'>
                <CardHeader>
                  <CardTitle>Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>
                    Vm creation per month in the last months
                  </CardDescription>
                  <VmCreationChart />
                </CardContent>
                <CardFooter className='text-foreground/50'>
                  This data is generated base on you user access level.
                </CardFooter>
              </Card>
              <Card className='col-span-1 lg:col-span-3'>
                <CardHeader>
                  <CardTitle>Recent task finished</CardTitle>
                  <CardDescription>
                    
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {/* <RecentSales /> */}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value='analytics' className='space-y-4'>
            <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
              <Card className='col-span-2 lg:col-span-2'>
                <CardHeader>
                  <CardTitle>Hypervisor Os</CardTitle>
                  <CardDescription>
                    All hypervisor os connected to system
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <HypervisorOsChart />
                </CardContent>
              </Card>
              <Card className='col-span-2 lg:col-span-2'>
                <CardHeader>
                  <CardTitle>VM current status</CardTitle>
                  <CardDescription>
                    
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <VMStatusChart />
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value='notifications' className='space-y-4'>
          </TabsContent>
        </Tabs>
      </Layout.Body>
    </Layout>
  );
}