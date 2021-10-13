import React, { ReactElement, ReactNode, useContext, useState } from 'react';
import { JsonSelection } from 'components/jsonSelection';
import { TagSelection } from 'components/tagSelection';
import { Alert, Button, Col, Form, Row } from 'react-bootstrap';
import { TermsOfServiceCheck } from 'components/termsOfServiceCheck';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { Benchmark, Flavor, Result, Site } from 'api';
import { postHelper } from 'api-helpers';
import { AxiosError } from 'axios';
import { SiteSearchPopover } from 'components/searchSelectors/siteSearchPopover';
import { BenchmarkSearchSelect } from 'components/searchSelectors/benchmarkSearchSelect';
import { FlavorSearchSelect } from 'components/searchSelectors/flavorSearchSelect';
import { getErrorMessage } from 'components/forms/getErrorMessage';

export function ResultSubmitForm(props: {
    onSuccess: () => void;
    onError: () => void;
}): ReactElement {
    const auth = useContext(UserContext);

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);
    const [tags, setTags] = useState<string[]>([]);
    const [termsOfServiceAccepted, setTermsOfServiceAccepted] = useState(false);
    const [fileContents, setFileContents] = useState<string | undefined>(undefined);

    const [errorMessage, setErrorMessage] = useState<ReactNode | undefined>(undefined);

    const { mutate } = useMutation(
        (data: Result) =>
            postHelper<Result>('/results', data, auth.token, {
                execution_datetime: '2020-05-21T10:31:00.000Z',
                benchmark_id: benchmark?.id,
                //site_id: site?.id,
                flavor_id: flavor?.id,
                tags_ids: tags,
            }),
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

    function isFormValid() {
        return (
            benchmark &&
            site &&
            flavor &&
            termsOfServiceAccepted &&
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
            {errorMessage !== undefined && <Alert variant="danger">Error: {errorMessage}</Alert>}
            <RegistrationCheck />
            <Form>
                <Form.Group className="mb-3">
                    <JsonSelection fileContents={fileContents} setFileContents={setFileContents} />{' '}
                </Form.Group>

                <Form.Group className="mb-3">
                    <BenchmarkSearchSelect benchmark={benchmark} setBenchmark={setBenchmark} />
                </Form.Group>

                <Form.Group className="mb-3">
                    <SiteSearchPopover site={site} setSite={setSite} />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Row>
                        <Col>Execution date:</Col>
                        <Col md="auto">
                            <DatePicker
                                selected={execDate}
                                onChange={(date) => setExecDate(date as Date | null)}
                                showTimeSelect
                                timeIntervals={15}
                                dateFormat="MMMM d, yyyy HH:mm"
                                timeFormat="HH:mm"
                            />
                        </Col>
                    </Row>
                    {/* dateFormat="Pp"*/}
                </Form.Group>

                <Form.Group className="mb-3">
                    <FlavorSearchSelect site={site} flavor={flavor} setFlavor={setFlavor} />
                </Form.Group>

                <Form.Group className="mb-1">
                    <TagSelection tags={tags} addTag={addTag} removeTag={removeTag} />
                </Form.Group>

                <Row className="align-items-center">
                    <Col>
                        <TermsOfServiceCheck
                            termsOfServiceAccepted={termsOfServiceAccepted}
                            setTermsOfServiceAccepted={setTermsOfServiceAccepted}
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
