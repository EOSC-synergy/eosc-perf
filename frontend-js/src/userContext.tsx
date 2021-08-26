import React from 'react';

export type UserInfo = {
    token?: string;
    email?: string;
    name?: string;
    admin: boolean;
};

export const emptyUser: UserInfo = {
    token: undefined,
    email: undefined,
    name: undefined,
    admin: false,
};

export const UserContext = React.createContext(emptyUser);
