import React, { ReactElement, useContext } from 'react';
import { UserContext } from 'userContext';
import { Alert } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import pages from 'pages';

export function RegistrationCheck(): ReactElement {
    const auth = useContext(UserContext);

    return (
        <>
            {!auth.registered && (
                <Alert variant="warning">
                    You must register before submitting data to the services on this website! Have a
                    look at the{' '}
                    <NavLink to={pages.RegistrationModule.path}>registration page</NavLink>.
                </Alert>
            )}
        </>
    );
}
