import React from 'react';
import { render, screen } from '@testing-library/react';
import { RegistrationCheck } from './registrationCheck';
import { UserContext, UserInfo } from './userContext';

const legalUser: UserInfo = {
    token: '__access__token__',
    email: 'email@example.com',
    registered: true,
    admin: true,
    loggedIn: true,
    loading: false,
};

describe('registration check', () => {
    test('no token', async () => {
        render(
            <UserContext.Provider value={{ ...legalUser, token: undefined }}>
                <RegistrationCheck />
            </UserContext.Provider>
        );

        const warning = screen.queryByText('You must register', { exact: false });
        expect(warning).toBeNull();
    });

    test('registered', async () => {
        render(
            <UserContext.Provider value={{ ...legalUser, registered: true }}>
                <RegistrationCheck />
            </UserContext.Provider>
        );

        const warning = screen.queryByText('You must register', { exact: false });
        expect(warning).toBeNull();
    });

    test('not registered', () => {
        render(
            <UserContext.Provider value={{ ...legalUser, registered: false }}>
                <RegistrationCheck />
            </UserContext.Provider>
        );

        const warning = screen.getByText('You must register', { exact: false });

        expect(warning).toBeInTheDocument();
    });
});
