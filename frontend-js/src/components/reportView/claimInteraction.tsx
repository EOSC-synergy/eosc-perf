import React, { ReactElement, useContext } from 'react';
import { Claim, Submit } from 'api';
import { useMutation } from 'react-query';
import { deleteHelper } from 'api-helpers';
import { Button } from 'react-bootstrap';
import { UserContext } from 'components/userContext';

export function ClaimInteraction(props: {
    claim: Claim;
    refetch: () => void;
    deleteText?: string;
}): ReactElement {
    const auth = useContext(UserContext);

    const endpoints = new Map<string, string>([
        [Submit.resource_type.BENCHMARK, '/benchmarks/'],
        [Submit.resource_type.SITE, '/sites/'],
        [Submit.resource_type.FLAVOR, '/flavors/'],
        [Submit.resource_type.CLAIM, '/reports/claims/'],
    ]);

    const { mutate: deleteClaim } = useMutation(
        () =>
            deleteHelper(
                (endpoints.get(props.claim.resource_type) ?? '/reports/claims') +
                    props.claim.resource_id,
                auth.token
            ),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    return (
        <>
            <Button
                variant="danger"
                onClick={() => {
                    deleteClaim();
                }}
            >
                {props.deleteText || 'Delete'}
            </Button>
        </>
    );
}
