import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, RouterProvider } from 'react-router-dom';
import { ThemeProvider } from 'layouts/ThemeLayout'
import { Toaster } from '@/components/ui/toaster'
import  { AuthProvider } from 'context/AuthContext';
import App from "App";

import 'styles/globals.css';
import 'utils/interceptors'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    // <React.StrictMode>
        <Router>
            <AuthProvider>
                <ThemeProvider>
                    <App />
                    <Toaster />
                </ThemeProvider>
            </AuthProvider>
        </Router>
    // </React.StrictMode>
);
  