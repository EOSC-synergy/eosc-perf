import React, { useContext, useState } from 'react';
import { Button, Card, Col, Container, Form, Row } from 'react-bootstrap';
import { TagSelection } from './tagSelection';
import { LicenseAgreementCheck } from './licenseAgreementCheck';
import { Benchmark, Flavor, Result, Site } from 'api';
import {
    BenchmarkSearchPopover,
    FlavorSearchPopover,
    SiteSearchPopover,
} from 'components/SearchPopover';
import { useMutation } from 'react-query';
import { postHelper } from 'api-helpers';
import { UserContext } from 'userContext';
import { JsonSelection } from './jsonSelection';
import { PageBase } from '../pageBase';

function ResultSubmission(props: { token: string }) {
    const auth = useContext(UserContext);

    const { mutate } = useMutation((data: Result) =>
        postHelper<Result>('/results', data, auth.token, {
            // TODO: execution datetime?
            execution_datetime: '2020-05-21T10:31:00.000Z',
            benchmark_id: benchmark?.id,
            site_id: site?.id,
            flavor_id: flavor?.id,
            // TODO: tags
        })
    );

    function allFieldsFilled() {
        return benchmark && site && flavor && licenseAgreementAccepted && fileContents;
    }

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);
    const [tags, setTags] = useState<string[]>([]);
    const [licenseAgreementAccepted, setLicenseAgreementAccepted] = useState(false);
    const [fileContents, setFileContents] = useState<string | undefined>(undefined);

    function addTag(tag: string) {
        if (tags.includes(tag)) {
            return;
        }
        setTags([...tags, ...[tag]]);
    }

    function removeTag(tag: string) {
        setTags(tags.filter((v, i, a) => v !== tag));
    }

    function submit() {
        if (!allFieldsFilled()) {
            return;
        }
        mutate(JSON.parse(fileContents!));
    }

    return (
        <Container>
            <input type="hidden" id="license" value="{{ license }}" />
            <h1>Upload Result</h1>
            <Form>
                <Card>
                    <Card.Body>
                        <JsonSelection
                            fileContents={fileContents}
                            setFileContents={setFileContents}
                        />
                        <BenchmarkSearchPopover benchmark={benchmark} setBenchmark={setBenchmark} />
                        <SiteSearchPopover site={site} setSite={setSite} />
                        <FlavorSearchPopover site={site} flavor={flavor} setFlavor={setFlavor} />
                        <TagSelection tags={tags} addTag={addTag} removeTag={removeTag} />
                        <Row>
                            <Col>
                                <LicenseAgreementCheck
                                    licenseAgreementAccepted={licenseAgreementAccepted}
                                    setLicenseAgreementAccepted={setLicenseAgreementAccepted}
                                />
                            </Col>
                            <Col md="auto">
                                <Button
                                    variant="success"
                                    className="me-1"
                                    disabled={!allFieldsFilled()}
                                    onClick={submit}
                                >
                                    Submit
                                </Button>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>
            </Form>
        </Container>
    );
}

const ResultSubmissionModule: PageBase = {
    path: '/result-submission',
    element: ResultSubmission,
    name: 'ResultSubmission',
    displayName: 'Result',
};

export default ResultSubmissionModule;
