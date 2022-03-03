import { Alert, Button, Form } from 'react-bootstrap';
import React, { ReactElement, ReactNode, useContext, useEffect, useState } from 'react';
import { UserContext } from 'components/userContext';
import { useMutation } from 'react-query';
import { CreateSite } from 'model';
import { postHelper } from 'components/api-helpers';
import { AxiosError } from 'axios';
import { getErrorMessage } from 'components/forms/getErrorMessage';
import { RegistrationCheck } from 'components/registrationCheck';
import { LoadingWrapper } from '../loadingOverlay';
import { LoginCheck } from '../loginCheck';

// TODO: do not show invalid on first load
//       use default state valid?

export function SiteSubmitForm(props: {
    onSuccess: () => void;
    onError: () => void;
}): ReactElement {
    const auth = useContext(UserContext);

    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [description, setDescription] = useState('');

    const [errorMessage, setErrorMessage] = useState<ReactNode | undefined>(undefined);

    useEffect(() => {
        setErrorMessage(undefined);
    }, []);

    const { mutate } = useMutation(
        (data: CreateSite) => postHelper<CreateSite>('/sites', data, auth.token),
        {
            onSuccess: () => {
                props.onSuccess();
            },
            onError: (error: Error | AxiosError) => {
                setErrorMessage(getErrorMessage(error));
                props.onError();
            },
        }
    );

    function isNameValid() {
        return name.length > 0;
    }

    function isAddressValid() {
        return address.length > 0;
    }

    function isFormValid() {
        return isNameValid() && isAddressValid() && auth.token !== undefined;
    }

    function onSubmit() {
        if (!isFormValid()) {
            return;
        }
        mutate({
            name,
            address,
            description: description.length ? description : null,
        });
    }

    return (
        <LoadingWrapper isLoading={auth.loading}>
            {errorMessage !== undefined && <Alert variant="danger">Error: {errorMessage}</Alert>}
            <LoginCheck message="You must be logged in to submit new sites!" />
            <RegistrationCheck />
            <Form>
                <Form.Group>
                    <Form.Label>Name:</Form.Label>
                    <Form.Control
                        placeholder="KIT SCC"
                        onChange={(e) => setName(e.target.value)}
                        isInvalid={!isNameValid()}
                    />
                </Form.Group>

                <Form.Group className="mt-3">
                    <Form.Label>Address</Form.Label>
                    <Form.Control
                        placeholder="https://www.scc.kit.edu/"
                        onChange={(e) => setAddress(e.target.value)}
                        isInvalid={!isAddressValid()}
                    />
                </Form.Group>

                <Form.Group className="mt-3">
                    <Form.Label>Description (optional):</Form.Label>
                    <Form.Control
                        placeholder="Add a description here."
                        onChange={(e) => setDescription(e.target.value)}
                        as="textarea"
                    />
                </Form.Group>

                <Button
                    variant="success"
                    onClick={onSubmit}
                    disabled={!isFormValid()}
                    className="mt-1"
                >
                    Submit
                </Button>
            </Form>
        </LoadingWrapper>
    );
}
