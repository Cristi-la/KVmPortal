import { AlertCircle, Play, Pause, Power, ZapOff, RefreshCw, CirclePause, CircleHelp } from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { toast } from "@/components/ui/use-toast"

function formatDate(
    dateStr: string | null | undefined,
    format: string = 'YYYY:MM:DD HH:mm'
  ): string {
    if (!dateStr) return '';
  
    const date = new Date(dateStr);
  
    if (isNaN(date.getTime())) return dateStr;
  
    const formatWith = (date: Date, format: string) => {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // getMonth is zero-based
      const year = String(date.getFullYear());
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
  
      return format
        .replace('DD', day)
        .replace('MM', month)
        .replace('YYYY', year)
        .replace('HH', hours)
        .replace('mm', minutes)
  };
  
  return formatWith(date, format);
}


const stateData: Record<string, { description: string; icon: JSX.Element }> = {
  'running': { description: 'The VM is currently running.', icon: <Play color="green" /> },
  'idle': { description: 'The VM is idle, not performing any tasks.', icon: <Pause color="orange" /> },
  'paused': { description: 'The VM is paused.', icon: <Pause color="yellow" /> },
  'in shutdown': { description: 'The VM is in the process of shutting down.', icon: <Power color="red" /> },
  'shut off': { description: 'The VM is powered off.', icon: <ZapOff color="gray" /> },
  'crashed': { description: 'The VM has crashed.', icon: <AlertCircle color="red" /> },
  'pm suspended': { description: 'The VM is in a power management suspended state.', icon: <CirclePause color="blue" className="animate-spin" /> },
  'transition': { description: 'The VM is in transition between states.', icon: <RefreshCw color="purple" /> },
  'no info': { description: 'No information is available about the state of VM.', icon: <CircleHelp color="aqua" /> },
};


function formatState(state:string|undefined): JSX.Element {
  if (!state || !stateData[state.toLowerCase()]) {
    return <span>Unknown</span>;
  }

  const { description, icon } = stateData[state.toLowerCase()];

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger>
          {icon}
        </TooltipTrigger>
        <TooltipContent>
          <p>{description}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}


const copyClipboard = (e: React.MouseEvent<HTMLTableCellElement>, value: string) => {
  const target = e.currentTarget;
  const text2copy = target.innerText || value;
  
  navigator.clipboard.writeText(text2copy)
    .then(() => {
      toast({description:`Copied: "${text2copy}"`});
    })
    .catch((err) => {
      toast({description: 'Failed to copy text to clipboard'});
    });

  if (!target) return;

  target.classList.add('animate-jump');

  setTimeout(() => {
    target.classList.remove('animate-jump');
  }, 500); 
};

export { formatDate, formatState, copyClipboard }