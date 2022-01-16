import React, { ReactElement } from 'react';
import { Result } from 'model';
import { Form } from 'react-bootstrap';
import { ResultCallbacks } from 'components/resultSearch/resultCallbacks';
import { Ordered } from 'components/ordered';

/**
 * Column to select result
 * @param {Result & {orderIndex: number}} result
 * @param {ResultCallbacks} callbacks
 * @returns {React.ReactElement}
 * @constructor
 */
export function CheckboxColumn({
    result,
    callbacks,
}: {
    result: Ordered<Result>;
    callbacks: ResultCallbacks;
}): ReactElement {
    // TODO: "switch" => "checkbox" once it's fixed in react-bootstrap
    return (
        <Form>
            <Form.Check
                type="switch"
                onChange={() => {
                    callbacks.isSelected(result)
                        ? callbacks.unselect(result)
                        : callbacks.select(result);
                }}
                checked={callbacks.isSelected(result)}
            />
        </Form>
    );
}
