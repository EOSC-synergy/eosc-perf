import React, { ReactElement, useContext } from 'react';
import { Result } from 'api';
import { Button, ButtonGroup } from 'react-bootstrap';
import { ResultOps } from '../resultOps';
import { Envelope, Exclamation, Hash, Trash } from 'react-bootstrap-icons';
import { UserContext } from 'userContext';
import { Ordered } from 'components/ordered';
import { useMutation } from 'react-query';
import { deleteHelper } from 'api-helpers';

export function ActionColumn(props: { result: Ordered<Result>; ops: ResultOps }): ReactElement {
    // TODO: CSS: figure out why button group taller than it should be

    const auth = useContext(UserContext);

    const { mutate: deleteResult } = useMutation(() =>
        deleteHelper('/results/' + props.result.id, auth.token)
    );

    return (
        <ButtonGroup size="sm">
            <Button
                variant="primary"
                onClick={() => {
                    props.ops.display(props.result);
                }}
            >
                <Hash />
            </Button>
            {auth.token !== undefined && (
                <Button
                    variant="warning"
                    onClick={() => {
                        props.ops.report(props.result);
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
