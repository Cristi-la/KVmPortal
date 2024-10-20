import { createContext, useState, useEffect, useCallback } from "react";
import { ApiService } from "@/api/services.gen";
import { TokenRefresh, ApiTokenCreateResponse } from "vedor/types.gen";
import { toast } from "@/components/ui/use-toast";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom';
import useLocalStorage from 'hooks/use-local-storage';
import axios from 'axios';
import { LoadingWrapper } from "layouts/wrapers/LoadingWrapper";

const AuthContext = createContext< any | null>(null);

export default AuthContext;

export const AuthProvider = ({children}: {children: React.ReactNode}) =>{
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState<any | null>(null);
    const [authTokens, setAuthTokens] = useLocalStorage<TokenRefresh | null>({
        key: "authTokens",  defaultValue: null,
    });
    
    
    const updateAuth = useCallback((data: TokenRefresh | null = null) => {
        setAuthTokens(data);
        (data) 
            ? setUser(jwtDecode(data.access))
            : setUser(null);
    }, [])


    const login = useCallback(async (username: string, password: string)=>{
        setLoading(true)
        ApiService.apiTokenCreate({ requestBody: { username: username, password: password } })
        .then((data: ApiTokenCreateResponse) => {
            updateAuth(data);
            setLoading(false)

            try {
                const params = new URLSearchParams(window.location.search);
                const redirectPath = params.get("redirect");
                navigate(redirectPath ? decodeURI(redirectPath) : "/");
            } catch (error) {
                navigate("/");
            }
            
            toast({
                title: "Authentication success",
                description: `Login at ${new Date().toLocaleString()}`,
                variant: "secondary",
            })
            
        })
        .catch((error) => {
            toast({
                title: "Authentication failed",
                description: "Incorrect username or password.",
                variant: "destructive",
            })
            
            setLoading(false)
        })
    }, [])

    const logout = useCallback(() => {
        updateAuth(null);
        navigate("/login");
    }, [])

    const refresh = useCallback(async () => {
        if (!authTokens) return;
        const response = await axios.post('/api/token/refresh/', {
            refresh: authTokens.refresh,
        });

        if (response.data) {
            updateAuth(response.data);
            return response.data;
        }
        return null;
    }, [])


    const context = {
        user:user,
        authTokens:authTokens,
        setAuthTokens:setAuthTokens,
        setUser:setUser,

        logout:logout,
        login:login,

        refresh:refresh,
        updateAuth:updateAuth
    }


    useEffect(()=> {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access))
            navigate('/')
        }
        setLoading(false)
    }, [])


    // useEffect(() => {
    //     window.addEventListener('authTokensUpdated', () => {
    //         const authTokens = JSON.parse(localStorage.getItem('authTokens')!);
    //         updateAuth(authTokens);
    //     })
    // }, [])

    return(
        <AuthContext.Provider value={context} >
            <LoadingWrapper loading={loading}>
                {children}
            </LoadingWrapper>
        </AuthContext.Provider>
    )
}