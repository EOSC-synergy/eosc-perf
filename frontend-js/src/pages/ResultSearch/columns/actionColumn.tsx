import { Result } from 'api';
import { Button, ButtonGroup } from 'react-bootstrap';
import { ResultOps } from '../resultOps';
import { Envelope, Exclamation, Hash, Trash } from 'react-bootstrap-icons';
import { useContext } from 'react';
import { UserContext } from 'userContext';

export function ActionColumn(props: { result: Result; ops: ResultOps }) {
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
                    <Button variant="secondary" onClick={() => {} /* TODO: mail button */} disabled>
                        <Envelope />
                    </Button>
                    <Button variant="danger" onClick={() => {} /* TODO: delete button */} disabled>
                        <Trash />
                    </Button>
                </>
            )}
        </ButtonGroup>
    );
}
