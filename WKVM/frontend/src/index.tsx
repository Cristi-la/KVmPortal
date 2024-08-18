import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from 'layouts/theme-provider'
import App from "./App";
import 'styles/globals.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
            <Router>
                <App />
            </Router>
        </ThemeProvider>
    </React.StrictMode>
);
  