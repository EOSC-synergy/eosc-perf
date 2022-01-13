import React, { ReactElement, useContext } from 'react';
import { Result } from 'model';
import { Button, ButtonGroup } from 'react-bootstrap';
import { ResultCallbacks } from 'components/resultSearch/resultCallbacks';
import { Envelope, Exclamation, Hash, Trash } from 'react-bootstrap-icons';
import { UserContext } from 'components/userContext';
import { Ordered } from 'components/ordered';
import { useMutation } from 'react-query';
import { deleteHelper } from 'components/api-helpers';

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

    const { mutate: deleteResult } = useMutation(() =>
        deleteHelper('/results/' + result.id, auth.token)
    );

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
                    <Button
                        variant="secondary"
                        onClick={() => undefined /* TODO: mail button */}
                        disabled
                    >
                        <Envelope />
                    </Button>
                    {/* TODO: visual feedback */}
                    <Button variant="danger" onClick={() => deleteResult()}>
                        <Trash />
                    </Button>
                </>
            )}
        </ButtonGroup>
    );
}
