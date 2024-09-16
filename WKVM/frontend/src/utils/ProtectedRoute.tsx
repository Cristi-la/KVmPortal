import { Route, Navigate, RouteProps,   } from "react-router-dom";
import { useNavigate, useLocation } from 'react-router-dom';
import React from 'react';
import { useContext } from "react";
import AuthContext from "context/AuthContext";


const ProtectedRoute = ({children}: {children: React.ReactNode}) => {
    const { user } = useContext(AuthContext)!;
    const location = useLocation();

    return user 
        ? children 
        : <Navigate to={`/login?redirect=${encodeURIComponent(location.pathname)}`} replace/>;
};

export default ProtectedRoute;