import { createContext, useState, useEffect } from "react";
import { ApiService } from "@/api/services.gen";
import { TokenRefresh } from "@/api/types.gen";
import { useToast } from "@/components/ui/use-toast";
import jwtDecode from "jwt-decode";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({children}: {children: React.ReactNode}) =>{
    let [ user, setUser ] = useState<string | null>(null);
    let [ authTokens, setAuthTokens ] = useState<TokenRefresh | null>(null);
    const { toast } = useToast();

    let login = async ()=>{
        ApiService.apiTokenCreate({ requestBody: { username: 'admin', password: 'admin' } })
        .then((data: TokenRefresh) => {
            setAuthTokens(data);
            setUser(jwtDecode(data.access));

            {
                toast({
                    title: "Success",
                    description: `Login at ${new Date().toLocaleString()}`,
                    variant: "secondary",
                })
            }

        }).catch((error) => {
            {
                toast({
                  title: "Error",
                  description: "Friday, February 10, 2023 at 5:57 PM",
                  variant: "destructive",
                })
            }
        })      
    }

    let contextData = {
        login: login,
        user: user,
    }

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}