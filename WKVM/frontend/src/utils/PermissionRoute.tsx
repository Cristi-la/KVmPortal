import { Route, Navigate, RouteProps,   } from "react-router-dom";
import { useNavigate, useLocation } from 'react-router-dom';
import React from 'react';


const PermissionRoute = ({children}: {children: any}) => {
    // const context = useLocation();

    // if (!context.user || !context.user?.permissions.includes('can_view_page'))
    //     return <Navigate to={`/401`} replace/>;

    // return children
};

export default PermissionRoute;