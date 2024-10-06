import ReactDOM from 'react-dom/client';
import React from 'react';
import { BrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';

import { Toaster } from '@/components/ui/toaster'
import 'styles/globals.css';
import 'utils/interceptors'

import  { AuthProvider } from 'context/AuthContext';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <BrowserRouter>
            <AuthProvider>
                <App />
            </AuthProvider>
            <Toaster />
        </BrowserRouter>
    </React.StrictMode>
);
  