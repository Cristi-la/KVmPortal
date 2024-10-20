import React, {
  createContext,
  useContext,
  useState,
  ReactNode,
  ChangeEvent,
  FC,
} from 'react';
// import type {InputProps} from '@/components/ui/input';
// import { Input } from '@/components/ui/input';
import { FloatingInput, FloatingLabel } from 'components/fields/floating-label-input';
import { Search } from 'lucide-react';

interface FieldContextType {
  searchTerm: string;
  setSearchTerm: React.Dispatch<React.SetStateAction<string>>;
}


const FieldContext = createContext<FieldContextType | undefined>(undefined);


export const useFieldContext = (): FieldContextType => {
  const context = useContext(FieldContext);
  if (!context) {
    throw new Error('useFieldContext must be used within a FieldProvider');
  }
  return context;
};


interface FieldProviderProps {
  children: ReactNode;
}

export const FieldProvider: FC<FieldProviderProps> = ({ children }) => {
  const [searchTerm, setSearchTerm] = useState<string>('');

  return (
    <FieldContext.Provider value={{ searchTerm, setSearchTerm }}>
      {children}
    </FieldContext.Provider>
  );
};



// export const FieldInput = React.forwardRef<HTMLInputElement, InputProps>(
//   ({...props }, ref) => {
//   const { setSearchTerm } = useFieldContext();

//   const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
//     setSearchTerm(e.target.value);
//   };

//   return (
//     <Input
//       onChange={handleChange}
//       ref={ref}
//       {...props}
//     />
//   );
// });

interface KeyProps {
  children: ReactNode;
}

export const Key: FC<KeyProps> = ({ children }) => {
  return <span className="font-bold">{children}</span>;
};

interface ValueProps {
  children: ReactNode;
}

export const Value: FC<ValueProps> = ({ children }) => {
  return <span>{children}</span>;
};

interface RecordProps {
  children: ReactNode;
}

export const Record: FC<RecordProps> = ({ children }) => {
  const { searchTerm } = useFieldContext();
  let keyText = '';
  let valueText = '';

  const extractTexts = (nodes: ReactNode) => {
    React.Children.forEach(nodes, (child) => {
      if (!React.isValidElement(child)) return;

      if (child.type === Key) {
        keyText += child.props.children;
      } else if (child.type === Value) {
        valueText += child.props.children;
      } else if (child.props && child.props.children) {
        extractTexts(child.props.children);
      }
    });
  };

  extractTexts(children);

  const search = searchTerm.toLowerCase().trim();
  const isVisible =
    keyText.toLowerCase().trim().includes(search) ||
    valueText.toLowerCase().trim().includes(search);

  return isVisible ? <div>{children}</div> : null;
};


export const SearchField = () => {
  const { setSearchTerm } = useFieldContext();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <>
      <FloatingInput id="floating" className="w-full" onChange={handleChange} />
      <FloatingLabel htmlFor="floating" className="flex flex-row items-center">
        <Search className="h-5 w-5 mr-1" />
        <div>Search for field / value</div>
      </FloatingLabel>
    </>
  );
};

