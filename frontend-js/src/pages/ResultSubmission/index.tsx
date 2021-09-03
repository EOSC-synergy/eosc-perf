import React, { useState } from 'react';
import { Button, Card, Col, Container, Form, Row } from 'react-bootstrap';
import { TagSelection } from './tagSelection';
import { LicenseAgreementCheck } from './licenseAgreementCheck';
import { Benchmark, Flavor, Site } from '../../api';
import {
    BenchmarkSearchPopover,
    FlavorSearchPopover,
    SiteSearchPopover,
} from '../../components/SearchPopover';

function FileSelection(props: { file?: File; setFile: (file: File) => void }) {
    return (
        <>
            <Form.Group>
                <Form.Label>Please select result JSON file</Form.Label>
                <Form.Control
                    type="file"
                    onChange={() => {} /*(e) => props.setFile(e.target.files[0])*/}
                />
            </Form.Group>
        </>
    );
}

function ResultSubmission(props: { token: string }) {
    function onSubmit() {
        // TODO
    }

    function allFieldsFilled() {
        return benchmark && site && flavor && licenseAgreementAccepted;
    }

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);
    const [tags, setTags] = useState<string[]>([]);
    const [licenseAgreementAccepted, setLicenseAgreementAccepted] = useState(false);
    const [file, setFile] = useState<File | undefined>(undefined);

    function addTag(tag: string) {
        if (tags.includes(tag)) {
            return;
        }
        setTags([...tags, ...[tag]]);
    }

    function removeTag(tag: string) {
        setTags(tags.filter((v, i, a) => v !== tag));
    }

    return (
        <Container>
            <input type="hidden" id="license" value="{{ license }}" />
            <h1>Upload Result</h1>
            <Form>
                <Card>
                    <Card.Body>
                        <FileSelection file={file} setFile={setFile} />
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

const ResultSubmissionModule = {
    path: '/result-submission',
    element: ResultSubmission,
    name: 'ResultSubmission',
    dropdownName: 'Result',
};

export default ResultSubmissionModule;
