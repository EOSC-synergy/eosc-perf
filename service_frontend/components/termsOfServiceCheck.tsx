import React, { useState } from 'react';
import { Badge, Button, Form, Modal } from 'react-bootstrap';
import { TermsOfService } from './termsOfService';
import actionable from '../styles/actionable.module.css';

/**
 * Form element component to make sure user has accepted terms of service
 * @param {boolean} props.accepted whether the terms of service have been accepted
 * @param {(accepted: boolean) => void} props.setAccepted set new acceptance state
 * @constructor
 */
export function TermsOfServiceCheck(props: {
    accepted: boolean;
    setAccepted: (accepted: boolean) => void;
}) {
    const [showTOS, setShowTOS] = useState(false);

    return (
        <>
            <Form.Group>
                <Form.Check
                    type="switch"
                    label={
                        <>
                            I have read and accept the{' '}
                            <Badge
                                bg="secondary"
                                onClick={() => setShowTOS(true)}
                                className={actionable.actionable}
                            >
                                Terms of Service
                            </Badge>
                        </>
                    }
                    checked={props.accepted}
                    onChange={() => props.setAccepted(!props.accepted)}
                />
            </Form.Group>
            <Modal show={showTOS} onHide={() => setShowTOS(false)} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>Acceptable Use Policy</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <TermsOfService />
                </Modal.Body>
                <Modal.Footer>
                    <Button
                        variant="success"
                        onClick={() => {
                            props.setAccepted(true);
                            setShowTOS(false);
                        }}
                    >
                        Accept
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}
