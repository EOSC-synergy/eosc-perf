import React, { ReactElement, useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Alert } from 'react-bootstrap';
import Link from 'next/link';

export function RegistrationCheck(): ReactElement {
    const auth = useContext(UserContext);

    return (
        <>
            {auth.token && !auth.registered && (
                <Alert variant='warning'>
                    You must register before submitting data to the services on this
                    website! Have a look at the{' '}
                    <Link href='/registration'>registration page</Link>.
                </Alert>
            )}
        </>
    );
}