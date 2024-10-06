"use client";

import * as React from "react";
import { CaretSortIcon, CheckIcon } from "@radix-ui/react-icons";
import { PopoverProps } from "@radix-ui/react-popover";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

import type { CancelablePromise } from '@/api/core/CancelablePromise';

interface ResultAbstract {
    id: string;
    name: string;
    description?: string;
}

interface Result extends ResultAbstract {
    xml: string;
    created: string;
    updated: string;
}

interface SearchSelectorProps {
    query: (...any: any) => CancelablePromise<any>; 
    query_detail: (...any: any) => CancelablePromise<any>; 
    intOptions?: Array<{ id: string; name: string }>
}

export function SearchSelector({ query, intOptions }: SearchSelectorProps) {
    const [ options, setOptions ] = React.useState(intOptions || [])
    const [ selected, setSelected] = React.useState<Result|null>(null);

    const refreshTags = React.useCallback(() => {
        if (!query) return;
        query().then((data) => {
          setOptions(data)
        })
      }, [query])
    
    React.useEffect(() => {refreshTags()}, [refreshTags])

    return (
        <Popover>
        <PopoverTrigger asChild>
            <Button
            variant="outline"
            size="sm"
            className="flex-1 justify-between md:max-w-[200px] lg:max-w-[300px]"
            >
            {selected ? selected.name : "Load templates..."}
            <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] p-0">
            <Command>
            <CommandInput placeholder="Search templates..." />
            <CommandEmpty>No presets found.</CommandEmpty>
            <CommandGroup heading="Examples">
                {options.map((option) => (
                <CommandItem
                    key={option.id}
                    onSelect={() => {
                        }}
                >
                    {option.name}
                    <CheckIcon
                    className={cn(
                        "ml-auto h-4 w-4",
                        option?.id === option.id
                        ? "opacity-100"
                        : "opacity-0",
                    )}
                    />
                </CommandItem>
                ))}
            </CommandGroup>
            </Command>
        </PopoverContent>
        </Popover>
    );
}