import React, { useState } from 'react';
import { Accordion, Button, Card, Col, Container, Row } from 'react-bootstrap';
import { LoadingOverlay } from '../../components/loadingOverlay';
import { useQuery } from 'react-query';
import { JSONPreviewModal } from './JSONPreviewModal';
import { ResultsPerPageSelection } from '../../components/resultsPerPageSelection';
import { CardAccordionToggle } from './cardAccordionToggle';
import { getHelper } from '../../api-helpers';
import { ResultTable } from './resultTable';
import { Benchmark, Flavor, Result, Results, Site } from '../../api';
import { Paginator } from '../../components/pagination';
import { DiagramView } from './diagramView';
import { ReportModal } from './reportModal';
import {
    SiteSearchPopover,
    BenchmarkSearchPopover,
    FlavorSearchPopover,
} from '../../components/SearchPopover';

const qs = require('qs');
const hash = require('object-hash');

function determineNotableKeys(benchmark: Benchmark) {
    // TODO: new json schema format parsing
    return [];

    function recurser(key: string, obj: any): string[] {
        if (key.startsWith('!') && typeof obj[key] !== 'object') {
            return [key.slice(1)];
        }

        if (typeof obj === 'object' && obj !== null) {
            return Object.entries(obj)
                .map(([k, v], _, __) => recurser(k, v)) // get all interesting children
                .reduce((acc: string[], arr: string[]) => [...acc, ...arr]) // make one array
                .map((path: string) => key + '.' + path); // prefix current key
        }
        return [];
    }

    return Object.entries(benchmark.json_schema)
        .map(([k, v], _, __) => recurser(k, v))
        .reduce((acc: string[], arr: string[]) => [...acc, ...arr]);
}

function ResultSearch(props: { initialBenchmark: string; location: { search: string } }) {
    /*const benchmarkId = qs.parse(props.location.search.slice(1)).benchmark || '';

    const benchmark = useQuery(
        'benchmark-' + benchmarkId,
        () => {
            return getHelper<Benchmark>('/benchmarks/' + benchmarkId);
        },
        {
            enabled: benchmarkId.length > 0,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );*/

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);

    /*const suggestedFields = benchmark.isSuccess
        ? determineNotableKeys(benchmark!.data.data)
        : undefined;*/
    const suggestedFields = benchmark ? determineNotableKeys(benchmark) : undefined;

    const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(1);
    // json preview modal
    const [showJSONPreview, setShowJSONPreview] = useState(false);

    const [showReportModal, setShowReportModal] = useState(false);

    // TODO: use map for performance?
    // TODO: maintain sorting
    const [selectedResults, setSelectedResults] = useState<Result[]>([]);

    const [previewResult, setPreviewResult] = useState<Result | null>(null);
    const [reportedResult, setReportedResult] = useState<Result | null>(null);

    // helpers for subelements
    const resultOps = {
        select: function (result: Result) {
            if (!this.isSelected(result)) {
                setSelectedResults([...selectedResults, result]);
            }
        },
        unselect: function (result: Result) {
            setSelectedResults(selectedResults.filter((r, i, a) => r.id !== result.id));
        },
        isSelected: function (result: Result) {
            return selectedResults.includes(result);
        },
        display: function (result: Result) {
            setPreviewResult(result);
            setShowJSONPreview(true);
        },
        report: function (result: Result) {
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
                flavor_id: flavor?.id,
            }),
        () => {
            return getHelper<Results>('/results', undefined, {
                per_page: resultsPerPage,
                page,
                benchmark_id: benchmark?.id,
                site_id: site?.id,
                flavor_id: flavor?.id,
            });
        },
        {
            enabled: true, //benchmarkId.length === 0 || benchmark.isSuccess,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    function search() {
        // TODO
    }

    function addFilter() {
        // TODO
    }

    // separate accordions to allow each element to be open simultaneously

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
                                        {/* TODO: Filters wrapper */}
                                        <ul
                                            id="filters"
                                            className="list-unstyled d-flex flex-column"
                                        ></ul>
                                        <Button variant="primary" onSubmit={search} disabled>
                                            Search
                                        </Button>
                                        <Button variant="success" onSubmit={addFilter} disabled>
                                            Add Filter
                                        </Button>
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
                    <div style={{ display: 'relative' }}>
                        {results.isSuccess && results.data!.data.total > 0 && (
                            <ResultTable
                                results={results.data!.data.items!}
                                ops={resultOps}
                                suggestions={suggestedFields}
                            />
                        )}
                        {results.isSuccess && results.data!.data.total == 0 && (
                            <div className="text-muted m-2">No results found! :(</div>
                        )}
                        {results.isError && 'Error while loading results'}
                        {results.isLoading && <LoadingOverlay />}
                    </div>
                    {/* fuck flexbox & CSS spacing */}
                    {results.isSuccess && (
                        <div className="m-2 d-flex">
                            <div
                                className="d-flex justify-content-start"
                                style={{ flex: 1, marginRight: 'auto' }}
                            >
                                <ResultsPerPageSelection
                                    onChange={setResultsPerPage}
                                    currentSelection={resultsPerPage}
                                />
                            </div>
                            <div className="d-flex justify-content-center" style={{ flex: 1 }}>
                                <Paginator pagination={results.data!.data} navigateTo={setPage} />
                            </div>
                            <div
                                className="d-flex justify-content-end"
                                style={{ flex: 1, marginLeft: 'auto' }}
                            >
                                <Button
                                    variant="primary"
                                    onClick={() => {}}
                                    className="m-2"
                                    disabled
                                >
                                    Invert Selection
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {}}
                                    className="m-2"
                                    disabled
                                >
                                    Select All
                                </Button>
                            </div>
                        </div>
                    )}
                </Card>
            </Container>
            <JSONPreviewModal
                show={showJSONPreview}
                closeModal={() => {
                    setShowJSONPreview(false);
                }}
                result={previewResult}
            />
            <ReportModal
                show={showReportModal}
                closeModal={() => {
                    setShowReportModal(false);
                }}
                result={reportedResult}
            />
        </>
    );
}

const ResultSearchModule = {
    path: '/result-search',
    element: ResultSearch,
    name: 'ResultSearch',
    dropdownName: 'Results',
};

export default ResultSearchModule;
