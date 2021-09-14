import React, { ReactElement, useContext, useState } from 'react';
import { Report } from 'api';
import { useMutation } from 'react-query';
import { patchHelper } from 'api-helpers';
import { Button } from 'react-bootstrap';
import { UserContext } from 'userContext';

export function ReportInteraction(props: {
    report: Report;
    refetch: () => void;
    approveText?: string;
    rejectText?: string;
}): ReactElement {
    // keep last state so we can re-enable one button if the other is pressed
    const [lastState, setLastState] = useState<boolean | undefined>(undefined);

    const auth = useContext(UserContext);

    const { mutate: approve, isSuccess: isApproved } = useMutation(
        () => patchHelper('/reports/' + props.report.id + '/approve', { accessToken: auth.token }),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    const { mutate: reject, isSuccess: isRejected } = useMutation(
        () => patchHelper('/reports/' + props.report.id + '/reject', { accessToken: auth.token }),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    return (
        <>
            <Button
                variant="success"
                onClick={() => {
                    approve();
                    setLastState(true);
                }}
                disabled={isApproved && lastState}
            >
                {props.approveText || 'Approve'}
            </Button>
            <Button
                variant="danger"
                onClick={() => {
                    reject();
                    setLastState(false);
                }}
                disabled={isRejected && !lastState}
            >
                {props.rejectText || 'Reject'}
            </Button>
        </>
    );
}
