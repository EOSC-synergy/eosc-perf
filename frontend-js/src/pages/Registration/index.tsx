import React, { ReactElement, useContext, useState } from 'react';
import { Alert, Button, Container } from 'react-bootstrap';
import { PageBase } from '../pageBase';
import { NavLink } from 'react-router-dom';
import { useMutation } from 'react-query';
import { postHelper } from 'api-helpers';
import { UserContext } from 'userContext';
import pages from 'pages';
import Highlight from 'react-highlight';

function Registration(): ReactElement {
    const auth = useContext(UserContext);

    const [error, setError] = useState<unknown | undefined>(undefined);

    const registration = useMutation(() => postHelper('/users:register', undefined, auth.token), {
        onSuccess: () => {
            // reset-redirect to refresh react-query from outside
            window.location.href = '/';
        },
        onError: (e) => {
            setError(e);
        },
    });

    return (
        <Container>
            {auth.registered && <Alert variant="primary">You are already registered!</Alert>}
            <h1>Registration</h1>
            To upload data to this website, you must register first.
            <hr />
            {error !== undefined && (
                <Alert variant="danger">
                    An error occured:{' '}
                    <Highlight className="json">{JSON.stringify(error, null, 4)}</Highlight>
                </Alert>
            )}
            I hereby acknowledge I have read and accepted the{' '}
            <NavLink to={pages.TermsOfServiceModule.path}>Terms of Use</NavLink>.<br />
            <Button onClick={() => registration.mutate()} disabled={registration.isSuccess}>
                Register
            </Button>
        </Container>
    );
}

const RegistrationModule: PageBase = {
    path: '/register',
    element: Registration,
    name: 'Registration',
    displayName: 'Registration',
};

export default RegistrationModule;
