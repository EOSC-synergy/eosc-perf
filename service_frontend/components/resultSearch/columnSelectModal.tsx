import React, { ReactElement, useState } from 'react';
import { Button, CloseButton, Col, ListGroup, Modal, Row } from 'react-bootstrap';
import { InputWithSuggestions } from 'components/inputWithSuggestions';
import { Suggestion } from './jsonSchema';

export function ColumnSelectModal(props: {
    show: boolean;
    closeModal: () => void;
    columns: string[];
    setColumns: (columns: string[]) => void;
    suggestions?: Suggestion[];
}): ReactElement {
    const [newColumn, setNewColumn] = useState('');
    const [activeColumns, setActiveColumns] = useState(props.columns);

    function addColumn() {
        if (newColumn.length > 0) {
            setActiveColumns([...activeColumns, newColumn]);
        }
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
                        <InputWithSuggestions
                            setInput={(input) => setNewColumn(input)}
                            placeholder="JSON.path.to"
                            suggestions={props.suggestions}
                        >
                            <Button variant="outline-success" onClick={addColumn}>
                                +
                            </Button>
                        </InputWithSuggestions>
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
                        setNewColumn('');
                    }}
                >
                    Close
                </button>
            </Modal.Footer>
        </Modal>
    );
}
