import React, { ReactElement, useContext, useState } from 'react';
import { Result } from 'model';
import { Button, Dropdown, Modal, SplitButton } from 'react-bootstrap';
import { ResultCallbacks } from 'components/resultSearch/resultCallbacks';
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
            <Dropdown.Item as="button" onClick={() => setShowModal(true)}>
                Delete
            </Dropdown.Item>
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
        <SplitButton variant="secondary" title="View" size="sm">
            {auth.loggedIn && (
                <Dropdown.Item
                    as="button"
                    onClick={() => {
                        callbacks.report(result);
                    }}
                >
                    Report
                </Dropdown.Item>
            )}
            {auth.loggedIn && auth.admin && (
                <ResultDeleter result={result} onDelete={callbacks.reload} />
            )}
        </SplitButton>
    );
    /*<Dropdown as={ButtonGroup}>
            <Button
                variant="primary"
                onClick={() => {
                    callbacks.display(result);
                }}
            >
                <Hash /> View
            </Button>

            <Dropdown.Toggle split variant="secondary" />
            <Dropdown.Menu>

            </Dropdown.Menu>
        </Dropdown>*/
    /*<ButtonGroup size="sm">
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
                </>
            )}
        </ButtonGroup>*/
}
