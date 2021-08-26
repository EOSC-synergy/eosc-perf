import React, { useState } from 'react';
import { Button, Col, FormControl, InputGroup, ListGroup, Modal, Row } from 'react-bootstrap';

export function ColumnSelectModal(props: {
    show: boolean;
    closeModal: (columns: string[]) => void;
    columns: string[];
}) {
    const [newColumn, setNewColumn] = useState('');
    const [activeColumns, setActiveColumns] = useState(props.columns);
    const [newColumns, setNewColumns] = useState(new Array<string>());

    function AddColumn() {
        setNewColumns([...newColumns, newColumn]);
    }

    return (
        <Modal show={props.show} onHide={props.closeModal}>
            <Modal.Header>
                <Modal.Title>Choose columns to display (drag &amp; drop)</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Row>
                    <Col>
                        <h4>Displayed columns:</h4>
                        <ListGroup>
                            {/* TODO: display columns, draggable */}
                            {/*activeColumns.map((c) => {
                                if (c in Default columns) {...} 
                            })*/}
                        </ListGroup>
                    </Col>
                    <Col>
                        <h4>Unused columns:</h4>
                        <ul id="otherAvailableColumns" className="list-group">
                            {/* TODO: display columns, draggable */}
                        </ul>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <h5>Color legend</h5>
                        <ListGroup horizontal={true}>
                            <ListGroup.Item variant="dark" className="list-group-item-small">
                                Required
                            </ListGroup.Item>
                            <ListGroup.Item variant="secondary" className="list-group-item-small">
                                System
                            </ListGroup.Item>
                            <ListGroup.Item variant="primary" className="list-group-item-small">
                                Suggested
                            </ListGroup.Item>
                        </ListGroup>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <h4>Add column</h4>
                        <InputGroup className="mb-3">
                            <FormControl
                                placeholder="JSON.path.to"
                                aria-label="New Column"
                                onChange={(e) => setNewColumn(e.target.value)}
                            />
                            <InputGroup.Append>
                                <Button variant="outline-success" onClick={AddColumn}>
                                    +
                                </Button>
                            </InputGroup.Append>
                        </InputGroup>
                    </Col>
                </Row>
            </Modal.Body>
            <Modal.Footer>
                <button type="button" className="btn btn-secondary" data-dismiss="modal">
                    Close
                </button>
            </Modal.Footer>
        </Modal>
    );
}
