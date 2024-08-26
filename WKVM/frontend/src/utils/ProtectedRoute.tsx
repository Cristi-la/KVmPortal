import { Route, Navigate, RouteProps,   } from "react-router-dom";
import { useNavigate, useLocation } from 'react-router-dom';
import React from 'react';


const ProtectedRoute = ({children}: {children: React.ReactNode}) => {
    const isAuthenticated: boolean = true;
    const location = useLocation();

    return isAuthenticated 
        ? children 
        : <Navigate to={`/login?redirect=${encodeURIComponent(location.pathname)}`} replace/>;
};

export default ProtectedRoute;