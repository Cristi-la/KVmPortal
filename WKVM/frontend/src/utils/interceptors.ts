import axios from 'axios';
import { OpenAPI } from '@/api';
import dayjs from 'dayjs';
import { jwtDecode } from 'jwt-decode';
import { toast } from '@/components/ui/use-toast';

let isRefreshing = false;
let subscribers: ((token: any) => void)[] = [];


const onRrefreshed = (token: any) => {
    subscribers.forEach((callback) => callback(token));
    subscribers = [];
};

// Function to add requests to the queue while refreshing
const addSubscriber = (callback: any) => {
    subscribers.push(callback);
};

OpenAPI.interceptors.request.use(async (request) => {
    let authTokens = JSON.parse(localStorage.getItem('authTokens')!);

    if (!authTokens) return request;

    const user = jwtDecode(authTokens.access);
    const isTokenValid = user?.exp && dayjs.unix(user.exp).isAfter(dayjs());

    if (isTokenValid) {
        if (request.headers) request.headers['Authorization'] = `Bearer ${authTokens.access}`;
        return request;
    }

    if (!isRefreshing) {
        isRefreshing = true;
        try {
            const response = await axios.post('/api/token/refresh/', { refresh: authTokens.refresh });
            authTokens = response.data;
            localStorage.setItem('authTokens', JSON.stringify(authTokens));

            isRefreshing = false;
            onRrefreshed(authTokens.access);

            if (request.headers) request.headers['Authorization'] = `Bearer ${authTokens.access}`;
            window.dispatchEvent(new Event("authTokensUpdated"));

            return request;

        } catch (error) {
            isRefreshing = false;
            subscribers = [];
            return Promise.reject(error);
        }
    }

    return new Promise((resolve) => {
        addSubscriber((newToken: string) => {
            if (request.headers) {
                request.headers['Authorization'] = `Bearer ${newToken}`;
            }
            resolve(request);
        });
    });
});

OpenAPI.interceptors.response.use(
    async (response) => {
        if (response?.status !== 200) {
            toast({
                title: "Error",
                description: response?.data?.detail || "An error occurred while processing your request.",
                variant: "destructive",
            });
        }
      
      return response
    }
);