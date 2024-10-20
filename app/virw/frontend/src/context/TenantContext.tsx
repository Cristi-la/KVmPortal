import { createContext, useState, useCallback, useContext,  } from "react";
import { ApiService } from "@/api/services.gen";
import { TokenRefresh, ApiTokenCreateResponse } from "vendpr/types.gen";
import { toast } from "@/components/ui/use-toast";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom';
import useLocalStorage from 'hooks/use-local-storage';
import AuthContext  from 'context/AuthContext';
import { LoadingWrapper } from "layouts/wrapers/LoadingWrapper";

const TenantContext = createContext< any | null>(null);
export default TenantContext;

export const TenantProvider = ({children}: {children: React.ReactNode}) =>{
    const { updateAuth, authTokens } = useContext(AuthContext);
    const [ tenant, setTenant ] = useState<string|null>(null);
    const [loading, setLoading] = useState(false);

    const changeTenat = useCallback(async (tenant_name: string)=>{
        ApiService.apiTokenTenantCreate({
            requestBody: {
                access: authTokens.access,
                refresh: authTokens.refresh,
                tenant: tenant_name
            }
        })
        .then((data) => {
            updateAuth(data);
            setTenant(tenant_name);
        }).catch((error) => {
            toast({
                title: "Tenant change failed",
                description: "Please try again.",
                variant: "destructive",
            })
        })
    },[authTokens])

    
    let context = {
        name: null,
        changeTenat: changeTenat,
    }

    return(
        <TenantContext.Provider value={context} >
            <LoadingWrapper loading={loading}>
                {children}
            </LoadingWrapper>
        </TenantContext.Provider>
    )
}