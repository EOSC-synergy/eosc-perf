import React, { ReactElement, useContext } from 'react';
import { Submit } from 'model';
import { useMutation } from 'react-query';
import { postHelper } from 'components/api-helpers';
import { Button } from 'react-bootstrap';
import { UserContext } from 'components/userContext';

export function SubmitInteraction(props: {
    submit: Submit;
    refetch: () => void;
    approveText?: string;
    rejectText?: string;
}): ReactElement {
    const auth = useContext(UserContext);

    const endpoints = new Map<string, string>([
        [Submit.resource_type.BENCHMARK, '/benchmarks/'],
        [Submit.resource_type.SITE, '/sites/'],
        [Submit.resource_type.FLAVOR, '/flavors/'],
        [Submit.resource_type.CLAIM, '/reports/claims/'],
    ]);

    const { mutate: approve } = useMutation(
        () =>
            postHelper<never>(
                (endpoints.get(props.submit.resource_type) ?? '/reports/claims') +
                    props.submit.resource_id +
                    ':approve',
                undefined,
                auth.token
            ),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    const { mutate: reject } = useMutation(
        () =>
            postHelper<never>(
                (endpoints.get(props.submit.resource_type) ?? '/reports/claims') +
                    props.submit.resource_id +
                    ':reject',
                undefined,
                auth.token
            ),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    return (
        <div className="mt-2">
            <Button
                variant="success"
                onClick={() => {
                    approve();
                }}
                className="me-1"
            >
                {props.approveText || 'Approve'}
            </Button>
            <Button
                variant="danger"
                onClick={() => {
                    reject();
                }}
            >
                {props.rejectText || 'Reject'}
            </Button>
        </div>
    );
}
