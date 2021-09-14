import { Alert, Button, Form } from 'react-bootstrap';
import React, { ReactElement, useContext, useEffect, useState } from 'react';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { SiteCreate } from 'api';
import { postHelper } from 'api-helpers';
import axios, { AxiosError } from 'axios';

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

    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    useEffect(() => {
        setErrorMessage(undefined);
    }, []);

    const { mutate } = useMutation(
        (data: SiteCreate) => postHelper<SiteCreate>('/sites', data, auth.token),
        {
            onSuccess: () => {
                props.onSuccess();
            },
            onError: (error: Error | AxiosError) => {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        switch (error.response.status) {
                            case 409:
                                setErrorMessage('Site already exists');
                                break;
                            case 422:
                            default:
                                setErrorMessage(
                                    'Could not process submission:' + error.response.data.message
                                );
                                break;
                        }
                    } else if (error.request) {
                        setErrorMessage('No response');
                    } else {
                        setErrorMessage(error.message);
                    }
                    // Access to config, request, and response
                } else {
                    // Just a stock error
                    setErrorMessage('Unknown error, check the console');
                }
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
            description: description.length ? description : undefined,
        });
    }

    return (
        <>
            {auth.token === undefined && (
                <Alert variant="danger">You must be logged in to submit new sites!</Alert>
            )}
            {errorMessage !== undefined && (
                <Alert variant="danger">{'Error: ' + errorMessage}</Alert>
            )}
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
        </>
    );
}
