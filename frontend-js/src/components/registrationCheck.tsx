import React, { ReactElement, useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Alert } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import RegistrationPage from 'pages/registration';

export function RegistrationCheck(): ReactElement {
    const auth = useContext(UserContext);

    return (
        <>
            {auth.token && !auth.registered && (
                <Alert variant="warning">
                    You must register before submitting data to the services on this website! Have a
                    look at the <NavLink to={RegistrationPage.path}>registration page</NavLink>.
                </Alert>
            )}
        </>
    );
}
