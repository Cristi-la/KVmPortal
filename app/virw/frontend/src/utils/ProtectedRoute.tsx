import { Navigate   } from "react-router-dom";
import {  useLocation } from 'react-router-dom';
import React from 'react';
import { useContext } from "react";
import AuthContext from "context/AuthContext";


const ProtectedRoute = ({children}: {children: React.ReactNode}) => {
    const { user } = useContext(AuthContext)!;
    const location = useLocation();
    
    const redir = (location.pathname !== '/')
        ? `?redirect=${encodeURIComponent(location.pathname)}`
        : '';

    return user 
        ? children 
        : <Navigate to={`/login${redir}`} replace/>;
};

export default ProtectedRoute;