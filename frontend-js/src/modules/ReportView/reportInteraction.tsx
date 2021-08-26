import { Report } from '../../api';
import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { patchHelper } from '../../api-helpers';
import { Button } from 'react-bootstrap';

export function ReportInteraction(props: {
    report: Report;
    token: string;
    refetch: () => void;
    approveText?: string;
    rejectText?: string;
}) {
    // keep last state so we can reenable one button if the other is pressed
    const [lastState, setLastState] = useState<boolean | undefined>(undefined);

    const { mutate: approve, isSuccess: isApproved } = useMutation(
        (data) =>
            patchHelper('/reports/' + props.report.id + '/approve', { accessToken: props.token }),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    const { mutate: reject, isSuccess: isRejected } = useMutation(
        (data) =>
            patchHelper('/reports/' + props.report.id + '/reject', { accessToken: props.token }),
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
