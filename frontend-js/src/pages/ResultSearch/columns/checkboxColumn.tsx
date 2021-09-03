import { Result } from 'api';
import { Form } from 'react-bootstrap';
import { ResultOps } from '../resultOps';

export function CheckboxColumn(props: { result: Result; ops: ResultOps }) {
    // TODO: "switch" => "checkbox" once it's fixed in react-bootstrap
    return (
        <Form>
            <Form.Check
                type="switch"
                onChange={() => {
                    props.ops.isSelected(props.result)
                        ? props.ops.unselect(props.result)
                        : props.ops.select(props.result);
                }}
                checked={props.ops.isSelected(props.result)}
            />
        </Form>
    );
}
