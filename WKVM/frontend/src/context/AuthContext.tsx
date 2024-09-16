import { createContext, useState, useEffect } from "react";
import { ApiService } from "@/api/services.gen";
import { TokenRefresh, ApiTokenCreateResponse } from "@/api/types.gen";
import { toast } from "@/components/ui/use-toast";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom';
import useLocalStorage from 'hooks/use-local-storage';

const AuthContext = createContext< any | null>(null);

export default AuthContext;

export const AuthProvider = ({children}: {children: React.ReactNode}) =>{
    const navigate = useNavigate();
    let [user, setUser] = useState<any | null>(null);
    let [authTokens, setAuthTokens] = useLocalStorage<TokenRefresh | null>({
        key: "authTokens",
        defaultValue: null,
    });
    
    let [loading, setLoading] = useState(true);

    const refreshData = (data: TokenRefresh | null = null) => {
        setAuthTokens(data);
        (data) 
            ? setUser(jwtDecode(data.access))
            : setUser(null);
    }


    

    let login = async (username: string, password: string)=>{
        ApiService.apiTokenCreate({ requestBody: { username: username, password: password } })
        .then((data: ApiTokenCreateResponse) => {
            refreshData(data);

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
        })
    }

    let logout = () => {
        refreshData(null);
        navigate("/login");
    };


    let contextData = {
        user:user,
        setAuthTokens:setAuthTokens,
        setUser:setUser,
        logout:logout,
        login:login,
        refreshData:refreshData
    }


    useEffect(()=> {

        if (authTokens) {
            setUser(jwtDecode(authTokens.access))
        }
        setLoading(false)


    }, [authTokens, loading])


    useEffect(() => {
        window.addEventListener('authTokensUpdated', () => {
            let authTokens = JSON.parse(localStorage.getItem('authTokens')!);
            setUser(jwtDecode(authTokens.access));
        })
    }, [])

    return(
        <AuthContext.Provider value={contextData} >
            {loading ? null : children}
        </AuthContext.Provider>
    )
}