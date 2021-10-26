import React, { ReactElement } from 'react';
import { Form } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import TermsOfServicePage from 'pages/termsOfService';

export function TermsOfServiceCheck(props: {
    termsOfServiceAccepted: boolean;
    setTermsOfServiceAccepted: (accepted: boolean) => void;
}): ReactElement {
    return (
        <Form.Check
            type="switch"
            label={
                <>
                    I have read and accept the{' '}
                    <NavLink to={TermsOfServicePage.path}>Terms of Service</NavLink>
                </>
            }
            checked={props.termsOfServiceAccepted}
            onChange={() => props.setTermsOfServiceAccepted(!props.termsOfServiceAccepted)}
        />
    );
}
