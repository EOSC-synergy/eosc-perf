import React from 'react';
import { Button, Modal } from 'react-bootstrap';

/*
    TODO: ask if the x in the corner is necessary (also for column select)
    <button type="button" className="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
 */

export function JSONPreviewModal(props: { show: boolean; closeModal: () => void }) {
    return (
        <Modal show={props.show} scrollable={true} size="lg" onHide={props.closeModal}>
            <Modal.Header>
                <Modal.Title>JSON Data</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <pre>
                    <code id="jsonPreviewContent" className="json rounded">
                        {/* TODO: highlight.js & passing data
                        https://github.com/bvaughn/react-highlight.js https://github.com/bvaughn/react-highlight.js/pull/23
                        */}
                    </code>
                </pre>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.closeModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
