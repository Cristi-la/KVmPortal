import { useContext, useEffect, ReactNode, useRef } from 'react';
import AuthContext from 'context/AuthContext'; // Adjust the import path
import dayjs from 'dayjs';
import { toast } from '@/components/ui/use-toast';
import { OpenAPI } from '@/api'

const OpenApiHandler = ({ children }: { children: ReactNode }) => {
  const { authTokens, user, updateAuth, refresh } = useContext(AuthContext);

  // Use refs to maintain state across re-renders
  const isRefreshing = useRef(false);
  const subscribers = useRef<((token: string) => void)[]>([]);

  const onRefreshed = (token: string) => {
    subscribers.current.forEach((callback) => callback(token));
    subscribers.current = [];
  };

  const addSubscriber = (callback: (token: string) => void) => {
    subscribers.current.push(callback);
  };

  useEffect(() => {
    const requestInterceptor = OpenAPI.interceptors.request.use(
      async (request) => {
        if (!authTokens) return request;

        const isTokenValid =
          user.exp && dayjs.unix(user.exp).isAfter(dayjs());

        if (isTokenValid) {
          if (request.headers)
            request.headers['Authorization'] = `Bearer ${authTokens.access}`;
          return request;
        }

        if (!isRefreshing.current) {
          isRefreshing.current = true;
          try {
            const tokens = await refresh();
            updateAuth(tokens);

            isRefreshing.current = false;
            onRefreshed(tokens.access);

            if (request.headers)
              request.headers['Authorization'] = `Bearer ${tokens.access}`;

            return request;
          } catch (error) {
            isRefreshing.current = false;
            subscribers.current = [];
            return Promise.reject(error);
          }
        }

        return new Promise((resolve, reject) => {
          addSubscriber((newToken: string) => {
            if (request.headers) {
              request.headers['Authorization'] = `Bearer ${newToken}`;
            }
            resolve(request);
          });
        });
      },
    );

    // const responseInterceptor = OpenAPI.interceptors.response.use(
    //   async (response) => {
    //       if (response?.status !== 200 && response?.data?.detail) {
    //           toast({
    //               title: "Error",
    //               description: response?.data?.detail || "An error occurred while processing your request.",
    //               variant: "destructive",
    //           });
    //       }
        
    //     return response
    //   }
    // );
    

    // return () => {
    //   OpenAPI.interceptors.request.eject(requestInterceptor);
    //   OpenAPI.interceptors.response.eject(responseInterceptor);
    // };
  }, [authTokens, user, updateAuth, refresh]);

  return children;
};

export default OpenApiHandler;
