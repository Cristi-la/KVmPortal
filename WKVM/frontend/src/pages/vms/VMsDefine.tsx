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
import { Button } from "@/components/ui/button";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { ApiService } from '@/api/services.gen';
import { SearchSelector } from 'components/fields/search-selector';

// import { CodeViewer } from "./components/code-viewer";
// import { MaxLengthSelector } from "./components/maxlength-selector";
// import { ModelSelector } from "./components/model-selector";
// import { PresetActions } from "./components/preset-actions";
// import { PresetSave } from "./components/preset-save";
// import { PresetSelector } from "./components/preset-selector";
// import { PresetShare } from "./components/preset-share";
// import { TemperatureSelector } from "./components/temperature-selector";
// import { TopPSelector } from "./components/top-p-selector";

export default function VMsDefine() {
    return (
        <Layout base>
            <Layout.Header >
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
                            <BreadcrumbPage>Define</BreadcrumbPage>
                        </BreadcrumbItem>
                    </BreadcrumbList>
                </Breadcrumb>

            </Layout.Header>
                

            <Layout.Body >
                <div className=''>
                    <div className="flex flex-col items-start justify-between space-y-2 py-4 md:flex-row md:items-center md:space-y-0 md:h-16">
                        <h2 className="text-lg font-semibold text-nowrap truncate w-full">Template creator</h2>
                        <div className="ml-auto flex w-full space-x-2 sm:justify-end">

                            <SearchSelector query={ApiService.apiTagList} query_detail={ApiService.apiTagRetrieve} />
                            <Button size='sm' variant='outline'>Load</Button>

                            <div className="hidden space-x-2 md:flex">
                                <Button size='sm' variant='outline'>Save</Button>
                                <Button size='sm' variant='outline'>Save As</Button>
                                <Button size='sm' variant='destructive'>Delete</Button>
                            </div>
                        </div>
                    </div>
                    <Separator />
                    <div>
                        <Tabs defaultValue="basic" className='h-full py-3'>
                            <TabsList className="flex flex-row mb-2">
                                <TabsTrigger value="basic" className='grow'>
                                    <span>Basic</span>
                                </TabsTrigger>
                                <TabsTrigger value="xml" className='grow'>
                                    <span>XML</span>
                                </TabsTrigger>
                                <TabsTrigger value="Tasks" className='grow'>
                                    <span>Storage</span>
                                </TabsTrigger>
                                <TabsTrigger value="Exec" className='grow'>
                                    <span>Exec</span>
                                </TabsTrigger>
                            </TabsList>
                            <div>
                                <TabsContent value="basic" className="flex h-full flex-col space-y-2">
                                    <div className="grid h-full grid-rows-2 gap-3 lg:grid-cols-2 lg:grid-rows-1">
                                        <Textarea
                                            placeholder="We're writing to [inset]. Congrats from OpenAI!"
                                            className="h-full min-h-[300px] lg:min-h-[700px] xl:min-h-[700px]"
                                        />
                                        <div className="rounded-md border bg-muted"></div>
                                    </div>
                                </TabsContent>
                                <TabsContent value="xml" className="mt-0 border-0 p-0">
                                    <Textarea
                                        className="min-h-[400px] flex-1 p-4 md:min-h-[700px] lg:min-h-[700px]"
                                    />
                                </TabsContent>
                                <TabsContent value="xml" className="mt-0 border-0 p-0">
                                </TabsContent>
                            </div>
                        </Tabs>
                        <div className="grid grid-flow-col justify-start gap-2">
                            <Button>Use</Button>
                            <Button variant='secondary'>Leave</Button>
                        </div>
                    </div>
                </div>

                {/* <div className="hidden h-full flex-col md:flex">
                    <div className="container flex flex-col items-start justify-between space-y-2 py-4 sm:flex-row sm:items-center sm:space-y-0 md:h-16">
                    <h2 className="text-lg font-semibold">Playground</h2>
                    <div className="ml-auto flex w-full space-x-2 sm:justify-end">
                        <PresetSelector presets={presets} />
                        <PresetSave />
                        <div className="hidden space-x-2 md:flex">
                        <CodeViewer />
                        <PresetShare />
                        </div>
                        <PresetActions />
                    </div>
                    </div>
                    <Separator />
                    <Tabs defaultValue="complete" className="flex-1">
                    <div className="container h-full py-6">
                        <div className="grid h-full items-stretch gap-6 md:grid-cols-[1fr_200px]">
                        <div className="hidden flex-col space-y-4 sm:flex md:order-2">
                            <div className="grid gap-2">
                            <HoverCard openDelay={200}>
                                <HoverCardTrigger asChild>
                                <span className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    Mode
                                </span>
                                </HoverCardTrigger>
                                <HoverCardContent className="w-[320px] text-sm" side="left">
                                Choose the interface that best suits your task. You can
                                provide: a simple prompt to complete, starting and ending
                                text to insert a completion within, or some text with
                                instructions to edit it.
                                </HoverCardContent>
                            </HoverCard>
                            <TabsList className="grid grid-cols-3">
                                <TabsTrigger value="complete">
                                <span className="sr-only">Complete</span>
 
                                </TabsTrigger>
                                <TabsTrigger value="insert">
                                <span className="sr-only">Insert</span>

                                </TabsTrigger>
                                <TabsTrigger value="edit">
                                <span className="sr-only">Edit</span>
                                </TabsTrigger>
                            </TabsList>
                            </div>
                            <ModelSelector types={types} models={models} />
                            <TemperatureSelector defaultValue={[0.56]} />
                            <MaxLengthSelector defaultValue={[256]} />
                            <TopPSelector defaultValue={[0.9]} />
                        </div>
                        <div className="md:order-1">
                            <TabsContent value="complete" className="mt-0 border-0 p-0">
                            <div className="flex h-full flex-col space-y-4">
                                <Textarea
                                placeholder="Write a tagline for an ice cream shop"
                                className="min-h-[400px] flex-1 p-4 md:min-h-[700px] lg:min-h-[700px]"
                                />
                                <div className="flex items-center space-x-2">
                                <Button>Submit</Button>
                                <Button variant="secondary">
                                    <span className="sr-only">Show history</span>
                                    <CounterClockwiseClockIcon className="h-4 w-4" />
                                </Button>
                                </div>
                            </div>
                            </TabsContent>
                            <TabsContent value="insert" className="mt-0 border-0 p-0">
                            <div className="flex flex-col space-y-4">
                                <div className="grid h-full grid-rows-2 gap-6 lg:grid-cols-2 lg:grid-rows-1">
                                <Textarea
                                    placeholder="We're writing to [inset]. Congrats from OpenAI!"
                                    className="h-full min-h-[300px] lg:min-h-[700px] xl:min-h-[700px]"
                                />
                                <div className="rounded-md border bg-muted"></div>
                                </div>
                                <div className="flex items-center space-x-2">
                                <Button>Submit</Button>
                                <Button variant="secondary">
                                    <span className="sr-only">Show history</span>
                                    <CounterClockwiseClockIcon className="h-4 w-4" />
                                </Button>
                                </div>
                            </div>
                            </TabsContent>
                            <TabsContent value="edit" className="mt-0 border-0 p-0">
                            <div className="flex flex-col space-y-4">
                                <div className="grid h-full gap-6 lg:grid-cols-2">
                                <div className="flex flex-col space-y-4">
                                    <div className="flex flex-1 flex-col space-y-2">
                                    <Label htmlFor="input">Input</Label>
                                    <Textarea
                                        id="input"
                                        placeholder="We is going to the market."
                                        className="flex-1 lg:min-h-[580px]"
                                    />
                                    </div>
                                    <div className="flex flex-col space-y-2">
                                    <Label htmlFor="instructions">Instructions</Label>
                                    <Textarea
                                        id="instructions"
                                        placeholder="Fix the grammar."
                                    />
                                    </div>
                                </div>
                                <div className="mt-[21px] min-h-[400px] rounded-md border bg-muted lg:min-h-[700px]" />
                                </div>
                                <div className="flex items-center space-x-2">
                                <Button>Submit</Button>
                                <Button variant="secondary">
                                    <span className="sr-only">Show history</span>
                                    <CounterClockwiseClockIcon className="h-4 w-4" />
                                </Button>
                                </div>
                            </div>
                            </TabsContent>
                        </div>
                        </div>
                    </div>
                    </Tabs>
                </div> */}
            </Layout.Body>
            <Layout.BaseFooter />
        </Layout>
    );
}
