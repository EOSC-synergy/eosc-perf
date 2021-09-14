import { JsonSelection } from 'pages/ResultSubmission/jsonSelection';
import {
    BenchmarkSearchPopover,
    FlavorSearchPopover,
    SiteSearchPopover,
} from 'components/SearchPopover';
import { TagSelection } from 'pages/ResultSubmission/tagSelection';
import { Alert, Button, Card, Col, Form, Row } from 'react-bootstrap';
import { LicenseAgreementCheck } from 'pages/ResultSubmission/licenseAgreementCheck';
import React, { useContext, useState } from 'react';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { Benchmark, Flavor, Result, Site } from 'api';
import { postHelper } from 'api-helpers';
import axios, { AxiosError } from 'axios';

export function ResultSubmitForm(props: { onSuccess: () => void; onError: () => void }) {
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

    function allFieldsFilled() {
        return benchmark && site && flavor && licenseAgreementAccepted && fileContents;
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
        if (!allFieldsFilled()) {
            return;
        }
        mutate(JSON.parse(fileContents!));
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
                <JsonSelection fileContents={fileContents} setFileContents={setFileContents} />
                <BenchmarkSearchPopover benchmark={benchmark} setBenchmark={setBenchmark} />
                <SiteSearchPopover site={site} setSite={setSite} />
                <FlavorSearchPopover site={site} flavor={flavor} setFlavor={setFlavor} />
                <TagSelection tags={tags} addTag={addTag} removeTag={removeTag} />

                <Row className="mt-2 align-items-center">
                    <Col>
                        <LicenseAgreementCheck
                            licenseAgreementAccepted={licenseAgreementAccepted}
                            setLicenseAgreementAccepted={setLicenseAgreementAccepted}
                        />
                    </Col>
                    <Col md="auto">
                        <Button variant="success" disabled={!allFieldsFilled()} onClick={submit}>
                            Submit
                        </Button>
                    </Col>
                </Row>
            </Form>
        </>
    );
}
