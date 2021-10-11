import React, { ReactElement, useContext } from 'react';
import { Result } from 'api';
import { Button, ButtonGroup } from 'react-bootstrap';
import { ResultOps } from '../resultOps';
import { Envelope, Exclamation, Hash, Trash } from 'react-bootstrap-icons';
import { UserContext } from 'userContext';
import { Ordered } from 'components/ordered';

export function ActionColumn(props: { result: Ordered<Result>; ops: ResultOps }): ReactElement {
    // TODO: CSS: figure out why button group taller than it should be

    const auth = useContext(UserContext);

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
            <Button
                variant="warning"
                onClick={() => {
                    props.ops.report(props.result);
                }}
            >
                <Exclamation />
            </Button>
            {auth.admin && (
                <>
                    <Button
                        variant="secondary"
                        onClick={() => undefined /* TODO: mail button */}
                        disabled
                    >
                        <Envelope />
                    </Button>
                    <Button
                        variant="danger"
                        onClick={() => undefined /* TODO: delete button */}
                        disabled
                    >
                        <Trash />
                    </Button>
                </>
            )}
        </ButtonGroup>
    );
}
