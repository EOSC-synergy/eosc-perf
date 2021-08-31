import React, { useState } from 'react';
import { Button, Card, Container, Form } from 'react-bootstrap';
import { BenchmarkSelection } from './benchmarkSelection';
import { SiteSelection } from './siteSelection';
import { TagSelection } from './tagSelection';
import { LicenseAgreementCheck } from './licenseAgreementCheck';

function FileSelection(props: { file?: File; setFile: (file: File) => void }) {
    return (
        <>
            <Form.File
                label="Please select result JSON file"
                onChange={() => {} /*(e) => props.setFile(e.target.files[0])*/}
            />
        </>
    );
}

function ResultSubmission(props: { token: string }) {
    function onSubmit() {
        // TODO
    }

    function allFieldsFilled() {
        return benchmarkId && siteId && flavorId && licenseAgreementAccepted;
    }

    const [benchmarkId, setBenchmarkId] = useState<string | undefined>(undefined);
    const [siteId, setSiteId] = useState<string | undefined>(undefined);
    const [flavorId, setFlavorId] = useState<string | undefined>();
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
                        <BenchmarkSelection benchmark={benchmarkId} setBenchmark={setBenchmarkId} />
                        <SiteSelection
                            siteId={siteId}
                            setSiteId={setSiteId}
                            flavorId={flavorId}
                            setFlavorId={setFlavorId}
                        />
                        <TagSelection tags={tags} addTag={addTag} removeTag={removeTag} />
                        <div className="d-flex justify-content-between">
                            <LicenseAgreementCheck
                                licenseAgreementAccepted={licenseAgreementAccepted}
                                setLicenseAgreementAccepted={setLicenseAgreementAccepted}
                            />
                            <Button
                                variant="success"
                                className="mr-1"
                                disabled={!allFieldsFilled()}
                            >
                                Submit
                            </Button>
                        </div>
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
