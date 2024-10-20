import * as React from "react";
import { useEffect, useState, useMemo } from "react";
import { Input, InputProps } from "@/components/ui/input";

interface DebouncedInputProps extends InputProps {
  value: string;
  onDebounceChange: (value: string) => void;
  debounceTime?: number;
}

const DebouncedInput: React.FC<DebouncedInputProps> = ({
  value: initialValue,
  onDebounceChange = () => {}, // No-op fallback
  debounceTime = 300,
  ...props
}) => {
  const [value, setValue] = useState<string>(initialValue);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setValue(initialValue);
    setLoading(false)
  }, [initialValue]);

  useEffect(() => {
    if (loading) return;

    const timeout = setTimeout(() => {
      onDebounceChange(value);
    }, debounceTime);

    return () => clearTimeout(timeout);
  }, [value]);

  return <Input 
    value={value ?? ''} 
    onChange={(e) => {
      if (e.target.value.length) 
      setValue(e.target.value);
    }}
    {...props} 
  />;
};

export { DebouncedInput };
