import { Form } from 'react-bootstrap';
import React from 'react';

export function LicenseAgreementCheck(props: {
    licenseAgreementAccepted: boolean;
    setLicenseAgreementAccepted: (accepted: boolean) => void;
}) {
    return (
        <Form.Check
            type="switch"
            label="I have read and accept the license agreement"
            checked={props.licenseAgreementAccepted}
            onChange={(e) => props.setLicenseAgreementAccepted(!props.licenseAgreementAccepted)}
        />
    );
}
