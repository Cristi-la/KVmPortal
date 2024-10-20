import ReactDOM from 'react-dom/client';
import React from 'react';
import { BrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';

import { Toaster } from '@/components/ui/toaster'
import 'styles/globals.css';
import { ThemeWrapper } from 'layouts/wrapers/ThemeWrapper'

import  { AuthProvider } from 'context/AuthContext';
import  { TenantProvider } from 'context/TenantContext';
import OpenApiHandler from 'utils/OpenApiHandler';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <BrowserRouter>
            <AuthProvider>
                <OpenApiHandler>
                    <TenantProvider>
                        <ThemeWrapper>
                            <App />
                        </ThemeWrapper>
                    </TenantProvider>
                </OpenApiHandler>
            </AuthProvider>
            <Toaster />
        </BrowserRouter>
    </React.StrictMode>
);

