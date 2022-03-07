import React, { ReactNode } from 'react';
import { useQuery } from 'react-query';
import { emptyUser, UserContext } from 'components/userContext';
import { getHelper } from 'components/api-helpers';
import { useAuth } from 'react-oidc-context';
import { User } from 'model';

/**
 * Wrapper to provide authentication info about the current user, such as email or token
 * @param children
 * @constructor
 */
export function UserContextWrapper({ children }: { children: ReactNode }) {
    const authentication = useAuth();

    const amIRegistered = useQuery(
        'registered',
        () => getHelper<User>('/users/self', authentication.user?.access_token),
        {
            retry: false,
            enabled: authentication.isAuthenticated,
        }
    );

    const amIAdmin = useQuery(
        'is_admin',
        () => {
            return getHelper<void>('/users/self:try_admin', authentication.user?.access_token);
        },
        {
            retry: false,
            enabled: authentication.user != null,
        }
    );

    const callbacks = {
        login: () => authentication.signinRedirect(),
        logout: () => authentication.removeUser(),
    };

    return (
        <UserContext.Provider
            value={
                authentication.isAuthenticated && authentication.user
                    ? {
                          token: authentication.user.access_token,
                          email: amIRegistered.data?.data.email,
                          registered: amIRegistered.isSuccess,
                          admin: amIAdmin.isSuccess,
                          loggedIn: true,
                          loading:
                              authentication.isLoading ||
                              amIRegistered.isLoading ||
                              amIAdmin.isLoading,
                          ...callbacks,
                      }
                    : { ...emptyUser, ...callbacks }
            }
        >
            {children}
        </UserContext.Provider>
    );
}
