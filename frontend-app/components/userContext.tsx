import React from 'react';

export type UserInfo = {
    token?: string;
    email?: string;
    admin: boolean;
    registered: boolean;
    loggedIn: boolean;
};

export const emptyUser: UserInfo = {
    token: undefined,
    email: undefined,
    admin: false,
    registered: false,
    loggedIn: false
};

export const UserContext = React.createContext(emptyUser);
