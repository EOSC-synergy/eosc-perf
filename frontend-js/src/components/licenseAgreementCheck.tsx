import React, { ReactElement } from 'react';
import { Form } from 'react-bootstrap';

export function LicenseAgreementCheck(props: {
    licenseAgreementAccepted: boolean;
    setLicenseAgreementAccepted: (accepted: boolean) => void;
}): ReactElement {
    return (
        <Form.Check
            type="switch"
            label="I have read and accept the license agreement"
            checked={props.licenseAgreementAccepted}
            onChange={() => props.setLicenseAgreementAccepted(!props.licenseAgreementAccepted)}
        />
    );
}
