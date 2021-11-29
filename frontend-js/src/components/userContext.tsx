import React from 'react';

export type UserInfo = {
    token?: string;
    email?: string;
    name?: string;
    admin: boolean;
    registered: boolean;
    loggedIn: boolean;
};

export const emptyUser: UserInfo = {
    token: undefined,
    email: undefined,
    name: undefined,
    admin: false,
    registered: false,
    loggedIn: false,
};

export const UserContext = React.createContext(emptyUser);
