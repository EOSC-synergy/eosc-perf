import React from 'react';
import { Button, Modal } from 'react-bootstrap';
import { Result } from 'model';
import { JsonHighlight } from 'components/jsonHighlight';

/**
 * Modal to view the JSON data of a result
 * @param {{result: Result | null, show: boolean, closeModal: () => void}} props
 * @constructor
 */
export function JsonPreviewModal(props: {
    result: Result | null;
    show: boolean;
    closeModal: () => void;
}) {
    return (
        <Modal show={props.show} scrollable={true} size="lg" onHide={props.closeModal}>
            <Modal.Header>
                <Modal.Title>JSON Data</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {props.result !== null && (
                    <JsonHighlight>{JSON.stringify(props.result.json, null, 4)}</JsonHighlight>
                )}
                {props.result == null && <div className="text-muted">Loading...</div>}
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.closeModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
