import React, { ReactElement, ReactNode, useContext, useEffect, useState } from 'react';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { CreateFlavor, Site } from 'api';
import { postHelper } from 'api-helpers';
import { AxiosError } from 'axios';
import { Alert, Button, Form } from 'react-bootstrap';
import { getErrorMessage } from 'components/forms/getErrorMessage';

// TODO: do not show invalid on first load
//       use default state valid?

export function FlavorSubmitForm(props: {
    site: Site;
    onSuccess: () => void;
    onError: () => void;
}): ReactElement {
    const auth = useContext(UserContext);

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');

    const [errorMessage, setErrorMessage] = useState<ReactNode | undefined>(undefined);

    // clear error message on load
    useEffect(() => {
        setErrorMessage(undefined);
    }, []);

    const { mutate } = useMutation(
        (data: CreateFlavor) =>
            postHelper<CreateFlavor>('/sites/' + props.site.id + '/flavors', data, auth.token),
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

    function isFormValid() {
        return isNameValid() && auth.token !== undefined;
    }

    function onSubmit() {
        if (!isFormValid()) {
            return;
        }
        mutate({
            name,
            description: description.length ? description : null,
        });
    }

    return (
        <>
            {auth.token === undefined && (
                <Alert variant="danger">You must be logged in to submit new site flavors!</Alert>
            )}
            {errorMessage !== undefined && <Alert variant="danger">Error: {errorMessage}</Alert>}
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Name:</Form.Label>
                    <Form.Control
                        placeholder="standard-medium"
                        onChange={(e) => setName(e.target.value)}
                        isInvalid={!isNameValid()}
                    />
                </Form.Group>

                <Form.Group>
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
