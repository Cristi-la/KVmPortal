import {Layout} from 'layouts/Layout'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "vendor/components/ui/breadcrumb"
import { toast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"
import { ToastAction } from "@/components/ui/toast"

import React, {useContext} from 'react';
import AuthContext from 'context/AuthContext'
import { ApiService } from 'vendor/api'

export default  function Home() {
  const { user } = useContext(AuthContext)!;

  return (
    <Layout fixed>
      <Layout.Header sticky>
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink href="/">Home</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbLink href="/components">Components</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>Breadcrumb</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

      </Layout.Header>

      <Layout.Body>
          {/* <span>{user.username}</span> */}

          <Button
            onClick={() => {
              toast({
                title: "Scheduled: Catch up",
                description: "Friday, February 10, 2023 at 5:57 PM",
                variant: "destructive",
                action: <ToastAction altText="Try again">Try again</ToastAction>,
              })
            }}
          >Success</Button>

          <Button
            onClick={() => {
              toast({
                title: "Scheduled: Catch up",
                description: "Friday, February 10, 2023 at 5:57 PM",
              })
            }}
          >Normal</Button>


          <Button
            onClick={() => {
              toast({
                title: "Scheduled: Catch up",
                description: "Friday, February 10, 2023 at 5:57 PM",
              })
            }}
          >Danger</Button>

          <Button
            onClick={() => {
              ApiService.apiVmList();
              
              console.log("user context", user.exp)
            }}
          >
            send q
          </Button>




          <form>
            <input type="text" />
            <input type="submit" value="dupa" />
          </form>

          
      </Layout.Body>
    </Layout>
  );
}