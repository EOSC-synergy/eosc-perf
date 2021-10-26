import React, { ReactElement } from 'react';
import { Result } from 'api';
import { Form } from 'react-bootstrap';
import { ResultOps } from 'components/resultSearch/resultOps';
import { Ordered } from 'components/ordered';

export function CheckboxColumn(props: { result: Ordered<Result>; ops: ResultOps }): ReactElement {
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
