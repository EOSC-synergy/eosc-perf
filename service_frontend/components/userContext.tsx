import React from 'react';

export type UserInfo = {
    /**
     * Access token for backend
     */
    token?: string;

    /**
     * Email as provided by user during EGI registration
     */
    email?: string;

    /**
     * Whether the user is an administrator (= EGI user has the required entitlements)
     */
    admin: boolean;

    /**
     * Whether the user has completed registration on the backend
     */
    registered: boolean;

    /**
     * Shorthand to check if the user is logged in
     */
    loggedIn: boolean;

    login: () => void;
    logout: () => void;
};

/**
 * Default/fallback user data when the user is not authenticated
 */
export const emptyUser: UserInfo = {
    token: undefined,
    email: undefined,
    admin: false,
    registered: false,
    loggedIn: false,
    login: () => {},
    logout: () => {},
};

export const UserContext = React.createContext(emptyUser);
