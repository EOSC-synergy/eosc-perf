import React, { ReactElement, ReactNode } from 'react';
import { useQuery } from 'react-query';
import { emptyUser, UserContext } from 'components/userContext';
import { getHelper } from 'api-helpers';
import { useAuth } from 'oidc-react';

export function UserContextWrapper(props: { children: ReactNode }): ReactElement {
    const authentication = useAuth();

    const amIRegistered = useQuery(
        'registered',
        () => getHelper('/users/self', authentication.userData?.access_token),
        {
            retry: false,
            enabled: authentication.userData != null,
        }
    );

    const amIAdmin = useQuery(
        'is_admin',
        () => {
            return getHelper<void>('/users/self:try_admin', authentication.userData?.access_token);
        },
        {
            retry: false,
            enabled: authentication.userData != null,
        }
    );

    return (
        <UserContext.Provider
            value={
                authentication.userData
                    ? {
                          token: authentication.userData.access_token,
                          name: authentication.userData.profile.name,
                          email: authentication.userData.profile.email,
                          registered: amIRegistered.isSuccess,
                          admin: amIAdmin.isSuccess,
                          loggedIn: true,
                      }
                    : emptyUser
            }
        >
            {props.children}
        </UserContext.Provider>
    );
}
