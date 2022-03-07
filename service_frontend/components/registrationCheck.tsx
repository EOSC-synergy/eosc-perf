import React, { useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Alert, Button, Col, Row } from 'react-bootstrap';
import Link from 'next/link';

/**
 * Warning banner that displays if the user has not completed registration
 * @constructor
 */
export function RegistrationCheck() {
    const auth = useContext(UserContext);

    return (
        <>
            {!auth.loading && auth.loggedIn && !auth.registered && (
                <Alert variant="warning">
                    <Row className="align-items-center">
                        <Col>
                            You must register before submitting data to the services on this
                            website!
                        </Col>
                        <Col md="auto">
                            <Link as={'a'} href="/registration" passHref>
                                <Button variant="secondary">Register</Button>
                            </Link>
                        </Col>
                    </Row>
                </Alert>
            )}
        </>
    );
}
