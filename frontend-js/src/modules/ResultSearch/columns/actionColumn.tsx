import { Result } from '../../../api';
import { Button, ButtonGroup } from 'react-bootstrap';
import { ResultOps } from '../resultOps';
import { Envelope, Exclamation, Hash, Trash } from 'react-bootstrap-icons';

export function ActionColumn(props: { result: Result; ops: ResultOps; admin: boolean }) {
    // TODO: CSS: figure out why button group taller than it should be

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
            <Button variant="warning" onClick={() => {} /* TODO: report button */}>
                <Exclamation />
            </Button>
            {props.admin && (
                <>
                    <Button variant="secondary" onClick={() => {} /* TODO: mail button */}>
                        <Envelope />
                    </Button>
                    <Button variant="danger" onClick={() => {} /* TODO: delete button */}>
                        <Trash />
                    </Button>
                </>
            )}
        </ButtonGroup>
    );
}
