import React, { ReactElement, useContext, useState } from 'react';
import { Alert, Button, Container } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { postHelper } from 'components/api-helpers';
import { UserContext } from 'components/userContext';
import { JsonHighlight } from 'components/jsonHighlight';
import Head from 'next/head';
import { TermsOfServiceCheck } from '../components/termsOfServiceCheck';

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
    const [termsOfServiceAccepted, setTermsOfServiceAccepted] = useState(false);

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
        <>
            <Head>
                <title>Registration</title>
            </Head>
            <Container>
                {auth.registered && <Alert variant="primary">You are already registered!</Alert>}
                <h1>Registration</h1>
                To upload data to this website, you must register first.
                <hr />
                {error !== undefined && (
                    <Alert variant="danger">
                        An error occured:{' '}
                        <JsonHighlight>{JSON.stringify(error, null, 4)}</JsonHighlight>
                    </Alert>
                )}
                <TermsOfServiceCheck
                    accepted={termsOfServiceAccepted}
                    setAccepted={setTermsOfServiceAccepted}
                />
                <Button
                    onClick={() => registration.mutate()}
                    disabled={registration.isSuccess || !termsOfServiceAccepted}
                >
                    Register
                </Button>
            </Container>
        </>
    );
}

export default Registration;
