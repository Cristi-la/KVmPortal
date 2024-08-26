import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from 'layouts/theme-provider'
import { Toaster } from '@/components/ui/toaster'
import cookie from "cookie";

import App from "App";
import 'styles/globals.css';
import { OpenAPI } from "@/api";
import  { AuthProvider } from 'context/AuthContext';


OpenAPI.interceptors.request.use((request) => {
    const { csrftoken } = cookie.parse(document.cookie);
    if (request.headers && csrftoken) {
      request.headers["X-CSRFTOKEN"] = csrftoken;
    }
    return request;
});


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
            <Router>
                <AuthProvider>
                    <App />
                </AuthProvider>
            </Router>
            <Toaster />
        </ThemeProvider>
    </React.StrictMode>
);
  