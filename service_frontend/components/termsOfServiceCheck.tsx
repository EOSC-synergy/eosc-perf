import React, { ReactElement } from 'react';
import { Form } from 'react-bootstrap';
import Link from 'next/link';

/**
 * Form element component to make sure user has accepted terms of service
 * @param {boolean} props.accepted whether the terms of service have been accepted
 * @param {(accepted: boolean) => void} props.setAccepted set new acceptance state
 * @constructor
 */
export function TermsOfServiceCheck(props: { accepted: boolean, setAccepted: (accepted: boolean) => void }) {
    return (
        <Form.Check
            type='switch'
            label={
                <>
                    I have read and accept the{' '}
                    <Link href='/terms-of-service'>Terms of Service</Link>
                </>
            }
            checked={props.accepted}
            onChange={() =>
                props.setAccepted(!props.accepted)
            }
        />
    );
}
