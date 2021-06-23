import React, { useState } from 'react';
import { Button, Card, CardColumns, Container, Form, InputGroup, ListGroup } from 'react-bootstrap';
import { useQuery } from 'react-query';
import axios, { AxiosResponse } from 'axios';
import { Result as BenchmarkResult } from '../BenchmarkSearch/types';

function FileSelection() {
    return (
        <Card>
            <Card.Body>
                <div className="m-2">
                    <label htmlFor="result_file">Please select result JSON file:</label>
                    <input type="file" className="form-control-file" id="result_file" name="file" />
                </div>
            </Card.Body>
        </Card>
    );
}

function BenchmarkSelection(props: { token: string }) {
    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'benchmarkSelect',
        () => {
            const endpoint = 'https://localhost/api/benchmarks';
            if (props.token !== undefined) {
                return axios.get<BenchmarkResult[]>(endpoint, {
                    headers: {
                        Authorization: 'Bearer ' + props.token,
                    },
                });
            }
            return axios.get<BenchmarkResult[]>(endpoint);
        },
        {
            enabled: !!props.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <Card>
            <Card.Body>
                <div className="m-2">
                    <Form.Group>
                        <Form.Label htmlFor="benchmark-selection">Select benchmark:</Form.Label>
                        <Form.Control as="select" id="benchmark-selection">
                            {isSuccess &&
                                data &&
                                data.data.map((benchmark) => (
                                    <option value={benchmark.id}>
                                        {benchmark.dockerImage}:{benchmark.dockerTag}
                                    </option>
                                ))}
                        </Form.Control>
                    </Form.Group>
                </div>
            </Card.Body>
        </Card>
    );
}

type SiteResult = {
    description: string;
    address: string;
    name: string;
    flavors: {
        description: string;
        name: string;
    }[];
    id: string;
};

function SiteSelection(props: { token: string }) {
    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'siteSelect',
        () => {
            const endpoint = 'https://localhost/api/sites';
            if (props.token !== undefined) {
                return axios.get<SiteResult[]>(endpoint, {
                    headers: {
                        Authorization: 'Bearer ' + props.token,
                    },
                });
            }
            return axios.get<SiteResult[]>(endpoint);
        },
        {
            enabled: !!props.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const [selectedSite, setSelectedSite] = useState<string | null>(null);
    const [selectedFlavor, setSelectedFlavor] = useState<string | null>(null);

    return (
        <Card>
            <Card.Body>
                <Form.Group>
                    <Form.Label htmlFor="site-selection">Select execution site:</Form.Label>
                    <Form.Control
                        as="select"
                        id="site-selection"
                        onChange={(e) => setSelectedSite(e.target.value)}
                    >
                        {isSuccess &&
                            data &&
                            data.data.map((site) => <option value={site.id}>{site.name}</option>)}
                    </Form.Control>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="site-flavor">Select machine flavor:</Form.Label>
                    <Form.Control
                        as="select"
                        id="site-flavor"
                        onChange={(e) => setSelectedFlavor(e.target.value)}
                    >
                        {selectedSite &&
                            data &&
                            data.data
                                .find((s) => s.id === selectedSite)!
                                .flavors.map((flavor) => (
                                    <option value={flavor.name}>{flavor.name} </option>
                                ))}
                    </Form.Control>
                </Form.Group>
                {/* TODO: add site button */}
                {/* <Form.Group>
                    <label htmlFor="siteFlavorCustom"></label>
                    <textarea
                        className="form-control d-none"
                        id="siteFlavorCustom"
                        name="siteFlavorCustom"
                        placeholder="Enter more details about your custom flavor here..."
                    ></textarea>
                </Form.Group>;
                <div id="customSiteInfo" className="d-none">
                    <div className="m-2">
                        <label htmlFor="site_name">Site name</label>
                        <br />
                        <input
                            type="text"
                            id="site_name"
                            className="form-control"
                            placeholder="KIT Cluster"
                            disabled
                        />
                    </div>
                    <div className="m-2">
                        <label htmlFor="site_address">Site address</label>
                        <br />
                        <input
                            type="text"
                            id="site_address"
                            className="form-control"
                            placeholder="cluster.kit.edu"
                            disabled
                        />
                    </div>
                    <div className="m-2">
                        <label htmlFor="site_description">Site description</label>
                        <br />
                        <input
                            type="text"
                            id="site_description"
                            className="form-control"
                            placeholder="Very good"
                            disabled
                        />
                    </div>
                    <div className="m-2">
                        <label htmlFor="customSiteFlavor">Machine flavor name:</label>
                        <br />
                        <input
                            type="text"
                            id="customSiteFlavor"
                            className="form-control"
                            placeholder="unknown"
                            disabled
                        />
                    </div>
                </div> */}
            </Card.Body>
        </Card>
    );
}

function TagSelection(props: { token: string }) {
    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'tagSelect',
        () => {
            const endpoint = 'https://localhost/api/tags';
            if (props.token !== undefined) {
                return axios.get<SiteResult[]>(endpoint, {
                    headers: {
                        Authorization: 'Bearer ' + props.token,
                    },
                });
            }
            return axios.get<SiteResult[]>(endpoint);
        },
        {
            enabled: !!props.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const [customTagName, setCustomTagName] = useState('');
    const [selectedTags, setSelectedTags] = useState<string[]>([]);

    function addCustomTag() {
        // TODO
    }

    function selectTag(tag: string) {
        setSelectedTags([...selectedTags, tag]);
    }

    function unselectTag(tag: string) {
        const index = selectedTags.indexOf(tag);
        if (index > -1) {
            setSelectedTags(selectedTags.splice(index, 1));
        }
    }

    return (
        <Card>
            <Card.Body>
                <Form.Group>
                    <Form.Label>Select tags:</Form.Label>
                    <div className="scrollable-dropdown">
                        <ListGroup>
                            {/* TODO: make this look nicer? */}
                            {isSuccess &&
                                data &&
                                (data.data.length > 0 ? (
                                    data.data.map((t) =>
                                        selectedTags.indexOf(t.id) > -1 ? (
                                            <ListGroup.Item onClick={(e) => unselectTag(t.id)}>
                                                {t.name}
                                            </ListGroup.Item>
                                        ) : (
                                            <ListGroup.Item onClick={(e) => selectTag(t.id)}>
                                                {t.name}
                                            </ListGroup.Item>
                                        )
                                    )
                                ) : (
                                    <ListGroup.Item disabled>No tags available.</ListGroup.Item>
                                ))}
                        </ListGroup>
                    </div>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="custom-tag">Custom tag</Form.Label>
                    <InputGroup>
                        <Form.Control
                            id="custom-tag"
                            placeholder="tensor"
                            onChange={(e) => setCustomTagName(e.target.value)}
                        />
                        <InputGroup.Append>
                            <Button
                                variant="success"
                                disabled={customTagName.length < 1}
                                onClick={addCustomTag}
                            >
                                Add Tag
                            </Button>
                        </InputGroup.Append>
                    </InputGroup>
                </Form.Group>
            </Card.Body>
        </Card>
    );
}

function LicenseAgreementCheck() {
    return (
        <label className="checkbox-label">
            {/* TODO: cannot use Form.Control because it makes the checkbox huge 
                          what ways around this? */}
            <input
                type="checkbox"
                className="checkbox"
                onChange={(e) => {
                    /* TODO */
                }}
            />{' '}
            I have read and accept the {/* TODO: show license modal */}
            <Button
                variant="secondary"
                onClick={() => {
                    alert('TODO');
                }}
            >
                License agreement
            </Button>
        </label>
    );
}

function ResultSubmission(props: { token: string }) {
    function onSubmit() {
        // TODO
    }

    function allFieldsFilled() {
        // TODO
        return false;
    }

    return (
        <Container>
            <input type="hidden" id="license" value="{{ license }}" />
            <h1>Upload Result</h1>
            <Form>
                <CardColumns>
                    <FileSelection />
                    <BenchmarkSelection token={props.token} />
                    <SiteSelection token={props.token} />
                    <TagSelection token={props.token} />
                </CardColumns>
                <LicenseAgreementCheck />
                <Button
                    variant="success"
                    className="float-right mr-1"
                    disabled={!allFieldsFilled()}
                >
                    Submit
                </Button>
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
