import React, { useState } from 'react';
import { Button, Card, Container, Form } from 'react-bootstrap';
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
