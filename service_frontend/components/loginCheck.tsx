import React, { useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Alert, Button, Col, Row } from 'react-bootstrap';

const DEFAULT_MESSAGE =
    'You must be logged in to submit data to the platform! Log in using the dropdown in the top right of the page.';

/**
 * Warning banner that displays if the user is not logged in.
 * @constructor
 */
export function LoginCheck({ message = DEFAULT_MESSAGE }: { message?: string }) {
    const auth = useContext(UserContext);

    return (
        <>
            {!auth.loading && !auth.loggedIn && (
                <Alert variant="danger">
                    <Row className="align-items-center">
                        <Col>{message}</Col>
                        <Col md="auto">
                            <Button onClick={auth.login} variant="secondary">
                                Login
                            </Button>
                        </Col>
                    </Row>
                </Alert>
            )}
        </>
    );
}
