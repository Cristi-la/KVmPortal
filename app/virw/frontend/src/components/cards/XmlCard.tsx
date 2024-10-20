
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
import type { XmlAbstract } from '@/api/types.gen'
import type { CancelablePromise } from '@/api/core/CancelablePromise';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState, useEffect, useCallback } from "react";
import XMLViewer from 'react-xml-viewer'
import { Skeleton } from "vendor/components/ui/skeleton";
import { Loader2, RefreshCcw } from "lucide-react"
import { Button } from "@/components/ui/button";

interface XmlsCardProps<T> {
    types: XmlAbstract[];
    get: (data: {id: number, xmlType: string}) => CancelablePromise<T>;
    hypervisor_id: number;
}

const XmlCard: React.FC<XmlsCardProps<any>> = ({ types, get, hypervisor_id }) => {
    const [rawXmls, setRawXmls] = useState<Record<string, string>>({});
    const [loadingXmls, setLoadingXmls] = useState<Record<string, boolean>>({});

    const getRawXml = useCallback((type: string) => {
        if (rawXmls[type] || loadingXmls[type]) {
            return;
        }
        setLoadingXmls((prevLoadingXmls) => ({
            ...prevLoadingXmls,
            [type]: true,
        }));

        get({ xmlType: type, id: hypervisor_id })
            .then((res) => {
                setRawXmls((prevRawXmls) => ({
                    ...prevRawXmls,
                    [type]: res.raw_xml, 
                }));
            }).finally(() => {
                setLoadingXmls((prevLoadingXmls) => ({
                    ...prevLoadingXmls,
                    [type]: false,
                }));
            });
    }, [rawXmls, get, hypervisor_id, loadingXmls]);

    useEffect(() => {
        if (types.length > 0) {
            getRawXml(types[0].xml_type as string);
        }
    }, [types]);

    return (
        <Tabs defaultValue={types.length > 0 ? types[0].xml_type : ''}>
            <TabsList className="flex flex-row mb-1">
                {types.map((xml: XmlAbstract) => (
                    xml.xml_type && (
                        <TabsTrigger
                        
                            key={xml.id}
                            value={xml.xml_type}
                            className="grow"
                            onClick={() => getRawXml(xml.xml_type as string)}
                        >
                            <span className="capitalize">{xml.xml_type}</span>
                            {
                                loadingXmls[xml.xml_type] ? (
                                    <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                                ) : null
                            }
                            
                        </TabsTrigger>
                    )
                ))}
            </TabsList>
            
                {types.map((xml: XmlAbstract) => (
                    xml?.xml_type && (
                        <TabsContent key={xml.id} value={xml.xml_type}>
                            <Card className="grow">
                                <CardContent className="m-0 p-4 relative">
                                    {rawXmls[xml.xml_type] ? (
                                        <>
                                            <Button 
                                                variant={'outline'}
                                                onClick={() => {
                                                    delete rawXmls[xml.xml_type as string]
                                                    getRawXml(xml.xml_type as string)
                                                }}
                                                className="absolute top-0 right-0 m-3 z-10"
                                                title="Refresh this XML file"
                                            >
                                                <RefreshCcw className="h-4 w-4" />
                                            </Button>
                                            <XMLViewer xml={rawXmls[xml.xml_type]} />
                                        </>
                                    ) : (
                                        <Skeleton className="flex items-center justify-center min-h-64 w-full">
                                            <p>Loading...</p>
                                        </Skeleton>
                                    )}
                                </CardContent>
                            </Card>
                        </TabsContent>
                    )
                ))}
        </Tabs>
    );
};

export default XmlCard;
