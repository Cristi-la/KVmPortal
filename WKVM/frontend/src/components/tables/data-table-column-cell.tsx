import { useState, useEffect, useRef } from 'react';
import { Badge } from '@/components/ui/badge';
import { TagAbstract } from '@/api/types.gen';

interface TagsCellProps<TData, TValue>
  extends React.HTMLAttributes<HTMLDivElement> {
    tags: Array<TagAbstract>;
}

export function ColumnCellTags<TData, TValue>({
    tags,
    ...props
  }: TagsCellProps<TData, TValue>) {
    if (!tags || tags.length === 0) {
      return null;
    }
    const MAX_VISIBLE_TAGS = 3;
    const hasHiddenTags = tags.length > MAX_VISIBLE_TAGS;
    const visibleTags = tags.slice(0, MAX_VISIBLE_TAGS);
    const hiddenTags = tags.slice(MAX_VISIBLE_TAGS);
  
    return (
      <div className="relative flex gap-2 whitespace-nowrap" {...props}>
        {/* Display the first few badges */}
        {visibleTags.map((tag: TagAbstract) => (
          <Badge
            key={tag.id}
            style={{ backgroundColor: tag.color }}
            className="px-1 py-0.5 text-xs text-nowrap mix-blend-difference"
          >
            {tag.name}
          </Badge>
        ))}
  
        {/* Ellipsis for hidden tags */}
        {hasHiddenTags && (
          <div className="relative group cursor-pointer">
            <span className="text-muted-foreground text-xs">...</span>
            {/* Hoverable container that shows only the hidden tags */}
            <div
              className="absolute left-0 top-full z-10 hidden group-hover:flex flex-wrap gap-1 bg-secondary p-2 rounded shadow-lg"
              style={{ minWidth: '150px' }}
            >
              {hiddenTags.map((tag: TagAbstract) => (
                <Badge
                  key={tag.id}
                  style={{ backgroundColor: tag.color }}
                  className="px-1 py-0.5 text-xs text-nowrap mix-blend-difference"
                >
                  {tag.name}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }