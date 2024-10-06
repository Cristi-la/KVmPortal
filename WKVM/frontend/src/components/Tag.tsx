import type { VariantProps } from "class-variance-authority"
import { Badge, badgeVariants } from "@/components/ui/badge"
import {cn} from "@/lib/utils"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import React, { useMemo } from 'react';
import type { TagAbstract } from "@/api/types.gen"
import { BadgePlus } from 'lucide-react';
import { Button } from '@/components/ui/button';

export interface TagProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
      desc?: string|null|undefined;
    }


function Tag({ children, className, variant, color, desc, ...props }: TagProps) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>
            <Badge
            className={cn(badgeVariants({ variant }), 'rounded-sm px-1 font-normal text-xs text-nowrap', className)}
            style={ (color) ? { backgroundColor: color } : {}} 
            {...props}
        >
            {children}
        </Badge>
        </TooltipTrigger>
        <TooltipContent>
          <h1 className="text-center font-bold" style={ (color) ? { color: color } : {}} >{children}</h1>
          { (desc) ? <p>{desc}</p> : <p>This tag does not have a description</p> }
          <p className="font-thin text-center">
            Hold to <span className="text-destructive">remove</span> this tag
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
    
  )
}

const TagComponent = ({ tags }: { tags: TagAbstract[] }) => {
  return useMemo(() => (
    <>
      {tags.map((tag: TagAbstract) => (
        <Tag key={tag.id} color={tag.color} desc={tag.description} className="text-sm">
          {tag.name}
        </Tag>
      ))}

      <Button variant='outline' className='size-6 p-1 border-dashed'>
        <BadgePlus/>
      </Button>
    </>
  ), [tags]);
};


export  { Tag, TagComponent }
