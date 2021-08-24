import { Result } from '../../../api';
import { Form } from 'react-bootstrap';
import { ResultOps } from '../resultOps';

export function CheckboxColumn(props: { result: Result; ops: ResultOps }) {
    return (
        <Form>
            <Form.Check
                type="checkbox"
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
