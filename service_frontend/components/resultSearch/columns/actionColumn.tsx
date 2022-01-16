import React, { ReactElement, useContext, useState } from 'react';
import { Result } from 'model';
import { Button, ButtonGroup, Modal } from 'react-bootstrap';
import { ResultCallbacks } from 'components/resultSearch/resultCallbacks';
import { Envelope, Exclamation, Hash, Trash } from 'react-bootstrap-icons';
import { UserContext } from 'components/userContext';
import { Ordered } from 'components/ordered';
import { useMutation } from 'react-query';
import { deleteHelper } from 'components/api-helpers';

function ResultDeleter({ result, onDelete }: { result: Result; onDelete: () => void }) {
    const auth = useContext(UserContext);

    const [showModal, setShowModal] = useState(false);

    const { mutate: deleteResult } = useMutation(
        () => deleteHelper('/results/' + result.id, auth.token),
        {
            onSuccess: onDelete,
        }
    );

    return (
        <>
            <Button variant="danger" onClick={() => setShowModal(true)}>
                <Trash />
            </Button>
            <Modal show={showModal} onHide={() => setShowModal(false)} size="lg" centered>
                <Modal.Header closeButton>
                    <Modal.Title>Delete result</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {/* display JSON? */}
                    Are you sure you want to delete this result?
                </Modal.Body>
                <Modal.Footer>
                    <Button
                        variant="danger"
                        onClick={() => {
                            deleteResult();
                            setShowModal(false);
                        }}
                    >
                        Delete
                    </Button>
                    <Button
                        variant="secondary"
                        onClick={() => {
                            setShowModal(false);
                        }}
                    >
                        Cancel
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}

/**
 * Column with buttons to interact with result
 * @param {Result & {orderIndex: number}} result
 * @param {ResultCallbacks} callbacks Callbacks for the operations
 * @returns {React.ReactElement}
 * @constructor
 */
export function ActionColumn({
    result,
    callbacks,
}: {
    result: Ordered<Result>;
    callbacks: ResultCallbacks;
}): ReactElement {
    // TODO: CSS: figure out why button group taller than it should be
    const auth = useContext(UserContext);

    return (
        <ButtonGroup size="sm">
            <Button
                variant="primary"
                onClick={() => {
                    callbacks.display(result);
                }}
            >
                <Hash />
            </Button>
            {auth.token !== undefined && (
                <Button
                    variant="warning"
                    onClick={() => {
                        callbacks.report(result);
                    }}
                >
                    <Exclamation />
                </Button>
            )}
            {auth.admin && (
                <>
                    <ResultDeleter result={result} onDelete={callbacks.reload} />
                    <Button
                        variant="secondary"
                        onClick={() => undefined /* TODO: mail button */}
                        disabled
                    >
                        <Envelope />
                    </Button>
                </>
            )}
        </ButtonGroup>
    );
}
