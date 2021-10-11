import React, { ReactElement, useState } from 'react';
import { Accordion, Button, Card, Col, Container, ListGroup, Row } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { useQuery } from 'react-query';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { ResultsPerPageSelection } from 'components/resultsPerPageSelection';
import { CardAccordionToggle } from './cardAccordionToggle';
import { getHelper } from 'api-helpers';
import { ResultTable } from './resultTable';
import { Benchmark, Flavor, Result, Results, Site } from 'api';
import { Paginator } from 'components/pagination';
import { DiagramView } from './diagramView';
import { ResultReportModal } from 'components/resultReportModal';
import {
    BenchmarkSearchPopover,
    FlavorSearchPopover,
    SiteSearchPopover,
} from 'components/searchPopover';
import { PageBase } from '../pageBase';
import { v4 as uuidv4 } from 'uuid';
import { Filter } from 'pages/ResultSearch/filter';
import { FilterEdit } from 'pages/ResultSearch/filterEdit';

import hash from 'object-hash';
import { Ordered } from 'components/ordered';

interface SchemaField {
    type?: string;
    suggestToUser?: boolean;
}

interface SchemaObject extends SchemaField {
    properties: { [key: string]: SchemaField };
}

function determineNotableKeys(benchmark: Benchmark): string[] {
    function recurser([key, field]: [string, SchemaField]): string[] {
        if (field.suggestToUser && field.type !== 'object') {
            return [key];
        }

        if (field.type === 'object') {
            return Object.entries((field as SchemaObject).properties)
                .map(recurser) // get all interesting children
                .reduce((acc: string[], arr: string[]) => [...acc, ...arr]) // make one array
                .map((path: string) => key + '.' + path); // prefix current key
        }
        return [];
    }

    const schema = benchmark.json_schema as SchemaObject;

    return Object.entries(schema.properties)
        .map(recurser)
        .reduce((acc: string[], arr: string[]) => [...acc, ...arr]);
}

function ResultSearch(): ReactElement {
    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);

    const [filters, setFilters] = useState<Map<string, Filter>>(new Map());

    function addFilter() {
        const newMap = new Map(filters); // shallow copy
        const id = uuidv4();
        newMap.set(id, {
            id,
            key: '',
            mode: '>',
            value: '',
        });
        setFilters(newMap);
    }

    function setFilter(id: string, key: string, mode: string, value: string) {
        const newMap = new Map(filters); // shallow copy
        newMap.set(id, {
            id,
            key,
            mode,
            value,
        });
        setFilters(newMap);
    }

    function deleteFilter(id: string) {
        const newMap = new Map(filters); // shallow copy
        newMap.delete(id);
        setFilters(newMap);
    }

    /*const suggestedFields = benchmark.isSuccess
        ? determineNotableKeys(benchmark!.data.data)
        : undefined;*/
    const suggestedFields = benchmark ? determineNotableKeys(benchmark) : undefined;

    const [resultsPerPage, setResultsPerPage] = useState(20);
    const [page, setPage] = useState(1);
    // json preview modal
    const [showJSONPreview, setShowJSONPreview] = useState(false);

    const [showReportModal, setShowReportModal] = useState(false);

    // TODO: use map for performance?
    // TODO: maintain sorting
    const [selectedResults, setSelectedResults] = useState<Ordered<Result>[]>([]);

    const [previewResult, setPreviewResult] = useState<Ordered<Result> | null>(null);
    const [reportedResult, setReportedResult] = useState<Ordered<Result> | null>(null);

    // helpers for subelements
    const resultOps = {
        select: function (result: Ordered<Result>) {
            if (!this.isSelected(result)) {
                // cannot call setSelectedResults directly, need to put in variable first
                const arr = [...selectedResults, result].sort(
                    (a, b) => a.orderIndex - b.orderIndex
                );
                setSelectedResults(arr);
            }
        },
        unselect: function (result: Ordered<Result>) {
            setSelectedResults(selectedResults.filter((r) => r.id !== result.id));
        },
        isSelected: function (result: Ordered<Result>) {
            return selectedResults.some((r) => r.id === result.id);
        },
        display: function (result: Ordered<Result>) {
            setPreviewResult(result);
            setShowJSONPreview(true);
        },
        report: function (result: Ordered<Result>) {
            setReportedResult(result);
            setShowReportModal(true);
        },
    };

    // hash used for queryKey to not have to add a dozen strings
    const results = useQuery(
        'results-' +
            resultsPerPage +
            '-' +
            hash({
                per_page: resultsPerPage,
                page,
                benchmark_id: benchmark?.id,
                site_id: site?.id,
                flavor_id: site !== undefined ? flavor?.id : undefined,
            }),
        () => {
            return getHelper<Results>('/results', undefined, {
                per_page: resultsPerPage,
                page,
                benchmark_id: benchmark?.id,
                site_id: site?.id,
                flavor_id: site !== undefined ? flavor?.id : undefined,
                filters: [...filters.keys()]
                    .map((k) => {
                        const filter = filters.get(k);
                        if (filter === undefined) {
                            return undefined;
                        }
                        if (filter.key.length === 0 || filter.value.length === 0) {
                            return undefined;
                        }
                        return filter.key + ' ' + filter.mode + ' ' + filter.value;
                    })
                    .filter((v?: string) => {
                        return v !== undefined;
                    }),
            });
        },
        {
            enabled: true, //benchmarkId.length === 0 || benchmark.isSuccess,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            <Container fluid="xl" className="mt-3">
                <Row>
                    <Col>
                        <Accordion defaultActiveKey="filters">
                            <Card>
                                <Card.Header>
                                    <CardAccordionToggle eventKey="filters">
                                        Filters
                                    </CardAccordionToggle>
                                </Card.Header>
                                <Accordion.Collapse eventKey="filters">
                                    <Card.Body>
                                        <BenchmarkSearchPopover
                                            benchmark={benchmark}
                                            setBenchmark={setBenchmark}
                                        />
                                        <SiteSearchPopover site={site} setSite={setSite} />
                                        <FlavorSearchPopover
                                            site={site}
                                            flavor={flavor}
                                            setFlavor={setFlavor}
                                        />
                                        <hr />
                                        <ListGroup variant="flush">
                                            {[...filters.keys()].map((key) => (
                                                <ListGroup.Item key={key}>
                                                    <FilterEdit
                                                        filter={filters.get(key)!}
                                                        setFilter={setFilter}
                                                        deleteFilter={deleteFilter}
                                                    />
                                                </ListGroup.Item>
                                            ))}
                                        </ListGroup>
                                        <div className="d-flex">
                                            <div
                                                className="justify-content-start"
                                                style={{ flex: 1, marginRight: 'auto' }}
                                            >
                                                <Button variant="success" onClick={addFilter}>
                                                    Add filter
                                                </Button>
                                            </div>
                                            <div
                                                className="d-flex justify-content-end"
                                                style={{ flex: 1, marginLeft: 'auto' }}
                                            >
                                                <Button onClick={() => results.refetch()}>
                                                    Apply filters
                                                </Button>
                                            </div>
                                        </div>
                                    </Card.Body>
                                </Accordion.Collapse>
                            </Card>
                        </Accordion>
                    </Col>
                    <Col>
                        <Accordion defaultActiveKey="diagram">
                            <Card>
                                <Card.Header>
                                    <CardAccordionToggle eventKey="diagram">
                                        Comparison diagram
                                    </CardAccordionToggle>
                                </Card.Header>
                                <Accordion.Collapse eventKey="diagram">
                                    <Card.Body>
                                        <DiagramView
                                            results={selectedResults}
                                            benchmark={benchmark}
                                            suggestions={suggestedFields}
                                        />
                                    </Card.Body>
                                </Accordion.Collapse>
                            </Card>
                        </Accordion>
                    </Col>
                </Row>
                <Card className="my-2">
                    <div>
                        {results.isSuccess && results.data && results.data.data.total > 0 && (
                            <ResultTable
                                results={results.data.data.items}
                                pageOffset={results.data.data.per_page * results.data.data.page}
                                ops={resultOps}
                                suggestions={suggestedFields}
                            />
                        )}
                        {results.isSuccess && results.data.data.total === 0 && (
                            <div className="text-muted m-2">No results found! :(</div>
                        )}
                        {results.isError && 'Error while loading results'}
                        {results.isLoading && <LoadingOverlay />}
                    </div>
                    {/* fuck flexbox & CSS spacing */}
                    {results.isSuccess && (
                        <div className="m-2 d-flex">
                            <div
                                className="justify-content-start"
                                style={{ flex: 1, marginRight: 'auto' }}
                            >
                                <ResultsPerPageSelection
                                    onChange={setResultsPerPage}
                                    currentSelection={resultsPerPage}
                                />
                            </div>
                            <div className="d-flex justify-content-center" style={{ flex: 1 }}>
                                <Paginator pagination={results.data.data} navigateTo={setPage} />
                            </div>
                            <div
                                className="d-flex justify-content-end"
                                style={{ flex: 1, marginLeft: 'auto' }}
                            >
                                <Button
                                    variant="primary"
                                    onClick={() => undefined}
                                    className="me-1"
                                    disabled
                                >
                                    Invert Selection
                                </Button>
                                <Button variant="primary" onClick={() => undefined} disabled>
                                    Select All
                                </Button>
                            </div>
                        </div>
                    )}
                </Card>
            </Container>
            {previewResult && (
                <JsonPreviewModal
                    show={showJSONPreview}
                    closeModal={() => {
                        setShowJSONPreview(false);
                    }}
                    result={previewResult}
                />
            )}
            {reportedResult && (
                <ResultReportModal
                    show={showReportModal}
                    closeModal={() => {
                        setShowReportModal(false);
                    }}
                    result={reportedResult}
                />
            )}
        </>
    );
}

const ResultSearchModule: PageBase = {
    path: '/result-search',
    element: ResultSearch,
    name: 'ResultSearch',
    displayName: 'Search',
};

export default ResultSearchModule;
