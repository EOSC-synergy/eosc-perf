import React, { ReactElement, useContext, useState } from 'react';
import { Alert, Button, Container } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { postHelper } from 'components/api-helpers';
import { UserContext } from 'components/userContext';
import Link from 'next/link';
import { JsonHighlight } from 'components/jsonHighlight';

/**
 * Page handling first-time user registration.
 *
 * Users are not automatically registered when logging in through EGI, they must register and accept our privacy policy
 * separately on this page.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function Registration(): ReactElement {
    const auth = useContext(UserContext);

    const [error, setError] = useState<unknown | undefined>(undefined);

    const registration = useMutation(
        () => postHelper('/users:register', undefined, auth.token),
        {
            onSuccess: () => {
                // reset-redirect to refresh react-query from outside
                window.location.href = '/';
            },
            onError: (e) => {
                setError(e);
            }
        }
    );

    return (
        <Container>
            {auth.registered && (
                <Alert variant='primary'>You are already registered!</Alert>
            )}
            <h1>Registration</h1>
            To upload data to this website, you must register first.
            <hr />
            {error !== undefined && (
                <Alert variant='danger'>
                    An error occured:{' '}
                    <JsonHighlight>
                        {JSON.stringify(error, null, 4)}
                    </JsonHighlight>
                </Alert>
            )}
            I hereby acknowledge I have read and accepted the{' '}
            <Link href='/terms-of-service'>Terms of Use</Link>.<br />
            <Button
                onClick={() => registration.mutate()}
                disabled={registration.isSuccess}
            >
                Register
            </Button>
        </Container>
    );
}

export default Registration;
