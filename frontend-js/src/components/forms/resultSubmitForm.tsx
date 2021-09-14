import React, { ReactElement, useContext, useState } from 'react';
import { JsonSelection } from 'pages/ResultSubmission/jsonSelection';
import {
    BenchmarkSearchPopover,
    FlavorSearchPopover,
    SiteSearchPopover,
} from 'components/searchPopover';
import { TagSelection } from 'pages/ResultSubmission/tagSelection';
import { Alert, Button, Col, Form, FormGroup, Row } from 'react-bootstrap';
import { LicenseAgreementCheck } from 'pages/ResultSubmission/licenseAgreementCheck';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { Benchmark, Flavor, Result, Site } from 'api';
import { postHelper } from 'api-helpers';
import axios, { AxiosError } from 'axios';

export function ResultSubmitForm(props: {
    onSuccess: () => void;
    onError: () => void;
}): ReactElement {
    const auth = useContext(UserContext);

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);
    const [tags, setTags] = useState<string[]>([]);
    const [licenseAgreementAccepted, setLicenseAgreementAccepted] = useState(false);
    const [fileContents, setFileContents] = useState<string | undefined>(undefined);

    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    const { mutate } = useMutation(
        (data: Result) =>
            postHelper<Result>('/results', data, auth.token, {
                // TODO: execution datetime?
                execution_datetime: '2020-05-21T10:31:00.000Z',
                benchmark_id: benchmark?.id,
                site_id: site?.id,
                flavor_id: flavor?.id,
                // TODO: tags
            }),
        {
            onSuccess: () => {
                props.onSuccess();
            },
            onError: (error: Error | AxiosError) => {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        switch (error.response.status) {
                            case 409:
                                setErrorMessage('Result already exists');
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

    function isFormValid() {
        return (
            benchmark &&
            site &&
            flavor &&
            licenseAgreementAccepted &&
            fileContents &&
            auth.token !== undefined
        );
    }

    function addTag(tag: string) {
        if (tags.includes(tag)) {
            return;
        }
        setTags([...tags, ...[tag]]);
    }

    function removeTag(tag: string) {
        setTags(tags.filter((v) => v !== tag));
    }

    function submit() {
        if (!isFormValid()) {
            return;
        }
        if (fileContents !== undefined) {
            mutate(JSON.parse(fileContents));
        }
    }

    return (
        <>
            {auth.token === undefined && (
                <Alert variant="danger">You must be logged in to submit new results!</Alert>
            )}
            {errorMessage !== undefined && (
                <Alert variant="danger">{'Error: ' + errorMessage}</Alert>
            )}
            <Form>
                <Form.Group className="mb-3">
                    <JsonSelection fileContents={fileContents} setFileContents={setFileContents} />{' '}
                </Form.Group>

                <Form.Group className="mb-3">
                    <BenchmarkSearchPopover benchmark={benchmark} setBenchmark={setBenchmark} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <SiteSearchPopover site={site} setSite={setSite} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <FlavorSearchPopover site={site} flavor={flavor} setFlavor={setFlavor} />
                </Form.Group>

                <Form.Group className="mb-1">
                    <TagSelection tags={tags} addTag={addTag} removeTag={removeTag} />
                </Form.Group>

                <Row className="align-items-center">
                    <Col>
                        <LicenseAgreementCheck
                            licenseAgreementAccepted={licenseAgreementAccepted}
                            setLicenseAgreementAccepted={setLicenseAgreementAccepted}
                        />
                    </Col>
                    <Col md="auto">
                        <Button variant="success" disabled={!isFormValid()} onClick={submit}>
                            Submit
                        </Button>
                    </Col>
                </Row>
            </Form>
        </>
    );
}
