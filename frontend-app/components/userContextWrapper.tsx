import React, { ReactElement, ReactNode } from 'react';
import { useQuery } from 'react-query';
import { emptyUser, UserContext } from 'components/userContext';
import { getHelper } from 'components/api-helpers';
import { useAuth } from 'react-oidc-context';
import { User } from 'model';

export function UserContextWrapper(props: {
    children: ReactNode;
}): ReactElement {
    const authentication = useAuth();

    const amIRegistered = useQuery(
        'registered',
        () => getHelper<User>('/users/self', authentication.user?.access_token),
        {
            retry: false,
            enabled: authentication.user != null
        }
    );

    const amIAdmin = useQuery(
        'is_admin',
        () => {
            return getHelper<void>(
                '/users/self:try_admin',
                authentication.user?.access_token
            );
        },
        {
            retry: false,
            enabled: authentication.user != null
        }
    );

    return (
        <UserContext.Provider
            value={
                authentication.user
                    ? {
                        token: authentication.user.access_token,
                        email: amIRegistered.data?.data.email,
                        registered: amIRegistered.isSuccess,
                        admin: amIAdmin.isSuccess,
                        loggedIn: true
                    }
                    : emptyUser
            }
        >
            {props.children}
        </UserContext.Provider>
    );
}
