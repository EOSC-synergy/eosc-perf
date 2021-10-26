import React, { ReactNode } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import { emptyUser, UserContext, UserInfo } from 'userContext';
import { getHelper } from 'api-helpers';

export function UserContextWrapper(props: { children: ReactNode }) {
    const whoAmI = useQuery('userInfo', () => axios.get<UserInfo>('/auth/whoami'), {
        retry: false,
    });

    const amIRegistered = useQuery(
        'registered',
        () => getHelper('/users/self', whoAmI.data?.data.token),
        {
            retry: false,
            enabled: whoAmI.isSuccess,
        }
    );

    return (
        <UserContext.Provider
            value={
                whoAmI.isSuccess
                    ? { ...whoAmI.data.data, registered: amIRegistered.isSuccess }
                    : emptyUser
            }
        >
            {props.children}
        </UserContext.Provider>
    );
}
