import React, { ReactElement, useState } from 'react';
import {
    Button,
    CloseButton,
    Col,
    FormControl,
    InputGroup,
    ListGroup,
    Modal,
    Row,
} from 'react-bootstrap';

export function ColumnSelectModal(props: {
    show: boolean;
    closeModal: () => void;
    columns: string[];
    setColumns: (columns: string[]) => void;
}): ReactElement {
    const [newColumn, setNewColumn] = useState('');
    const [activeColumns, setActiveColumns] = useState(props.columns);

    function addColumn() {
        setActiveColumns([...activeColumns, newColumn]);
    }

    function removeColumn(column: string) {
        setActiveColumns(activeColumns.filter((c) => c !== column));
    }

    return (
        <Modal show={props.show} onHide={props.closeModal}>
            <Modal.Header>
                <Modal.Title>Choose columns to display{/*(drag &amp; drop)*/}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Row>
                    <Col>
                        Displayed columns:
                        <ListGroup>
                            {/* TODO: draggable/sortable */}
                            {activeColumns.length === 0 && (
                                <ListGroup.Item>
                                    <div className="text-muted">No columns</div>
                                </ListGroup.Item>
                            )}
                            {activeColumns.map((column) => (
                                <ListGroup.Item key={column}>
                                    <Row>
                                        <Col>{column}</Col>
                                        <Col md="auto">
                                            <CloseButton onClick={() => removeColumn(column)} />
                                        </Col>
                                    </Row>
                                </ListGroup.Item>
                            ))}
                        </ListGroup>
                    </Col>
                </Row>
                <Row className="mt-2">
                    <Col>
                        Add column
                        <InputGroup>
                            <FormControl
                                placeholder="JSON.path.to"
                                aria-label="New Column"
                                onChange={(e) => setNewColumn(e.target.value)}
                            />
                            <Button variant="outline-success" onClick={addColumn}>
                                +
                            </Button>
                        </InputGroup>
                    </Col>
                </Row>
            </Modal.Body>
            <Modal.Footer>
                <button
                    type="button"
                    className="btn btn-secondary"
                    data-dismiss="modal"
                    onClick={() => {
                        props.closeModal();
                        props.setColumns(activeColumns);
                    }}
                >
                    Close
                </button>
            </Modal.Footer>
        </Modal>
    );
}
