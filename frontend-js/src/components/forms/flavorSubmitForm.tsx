import React, { useContext, useEffect, useState } from 'react';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { FlavorCreate, Site } from 'api';
import { postHelper } from 'api-helpers';
import axios, { AxiosError } from 'axios';
import { Alert, Button, Form } from 'react-bootstrap';

// TODO: do not show invalid on first load
//       use default state valid?

export function FlavorSubmitForm(props: {
    site: Site;
    onSuccess: () => void;
    onError: () => void;
}) {
    const auth = useContext(UserContext);

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');

    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    // clear error message on load
    useEffect(() => {
        setErrorMessage(undefined);
    });

    const { mutate } = useMutation(
        (data: FlavorCreate) =>
            postHelper<FlavorCreate>('/sites/' + props.site.id + '/flavors', data, auth.token),
        {
            onSuccess: () => {
                props.onSuccess();
            },
            onError: (error: Error | AxiosError) => {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        switch (error.response.status) {
                            case 409:
                                setErrorMessage('Flavor already exists');
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

    function isFormValid() {
        return isNameValid() && auth.token !== undefined;
    }

    function onSubmit() {
        if (!isFormValid()) {
            return;
        }
        mutate({
            name,
            description: description.length ? description : undefined,
        });
    }

    return (
        <>
            {auth.token === undefined && (
                <Alert variant="danger">You must be logged in to submit new site flavors!</Alert>
            )}
            {errorMessage !== undefined && (
                <Alert variant="danger">{'Error: ' + errorMessage}</Alert>
            )}
            <Form>
                <Form.Group>
                    <Form.Label>Name:</Form.Label>
                    <Form.Control
                        placeholder="standard-medium"
                        onChange={(e) => setName(e.target.value)}
                        isInvalid={!isNameValid()}
                    />
                </Form.Group>
                <Form.Label>Description (optional):</Form.Label>
                <Form.Control
                    placeholder="Add a description here."
                    onChange={(e) => setDescription(e.target.value)}
                    as="textarea"
                />
                <Button
                    variant="success"
                    onClick={onSubmit}
                    disabled={!isFormValid()}
                    className="my-1"
                >
                    Submit
                </Button>
            </Form>
        </>
    );
}
