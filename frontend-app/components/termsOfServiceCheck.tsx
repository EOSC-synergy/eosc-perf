import React, { ReactElement } from 'react';
import { Form } from 'react-bootstrap';
import Link from 'next/link';

export function TermsOfServiceCheck(props: {
    termsOfServiceAccepted: boolean;
    setTermsOfServiceAccepted: (accepted: boolean) => void;
}): ReactElement {
    return (
        <Form.Check
            type='switch'
            label={
                <>
                    I have read and accept the{' '}
                    <Link href='/terms-of-service'>Terms of Service</Link>
                </>
            }
            checked={props.termsOfServiceAccepted}
            onChange={() =>
                props.setTermsOfServiceAccepted(!props.termsOfServiceAccepted)
            }
        />
    );
}
