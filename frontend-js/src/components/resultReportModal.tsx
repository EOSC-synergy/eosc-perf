import React, { ReactElement, useContext, useState } from 'react';
import { CreateClaim, Result } from 'api';
import { Button, Form, Modal } from 'react-bootstrap';
import Highlight from 'react-highlight';
import { useMutation } from 'react-query';
import { postHelper } from 'api-helpers';
import { UserContext } from 'userContext';

export function ResultReportModal(props: {
    result: Result | null;
    show: boolean;
    closeModal: () => void;
}): ReactElement {
    const [message, setMessage] = useState('');

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: CreateClaim) =>
            postHelper<CreateClaim>('/results/' + props.result?.id + ':claim', data, auth.token, {
                result_id: props.result?.id,
            }),
        {
            onSuccess: () => {
                props.closeModal();
            },
        }
    );

    function submitReport() {
        mutate({ message });
    }

    return (
        <Modal show={props.show} scrollable={true} size="lg" onHide={props.closeModal}>
            <Modal.Header>
                <Modal.Title>Report result</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {props.result !== null && (
                    <Highlight className="json">
                        {JSON.stringify(props.result.json, null, 4)}
                    </Highlight>
                )}
                {props.result == null && <div className="text-muted">Loading...</div>}
                <Form>
                    <Form.Group>
                        <Form.Label>Report message</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Unrealistic results"
                            onChange={(e) => setMessage(e.target.value)}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="danger" onClick={submitReport}>
                    Submit
                </Button>
                <Button variant="secondary" onClick={props.closeModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
