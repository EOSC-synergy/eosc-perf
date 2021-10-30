import React, { ReactElement, useState } from 'react';
import { Accordion, Button, Card, Col, Container, ListGroup, Row } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { useQuery } from 'react-query';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { ResultsPerPageSelection } from 'components/resultsPerPageSelection';
import { CardAccordionToggle } from 'components/cardAccordionToggle';
import { getHelper } from 'api-helpers';
import { ResultTable } from 'components/resultSearch/resultTable';
import { Benchmark, Flavor, Result, Results, Site } from 'api';
import { Paginator } from 'components/pagination';
import { DiagramView } from 'components/resultSearch/diagramView';
import { ResultReportModal } from 'components/resultReportModal';
import { Page } from 'pages/page';
import { v4 as uuidv4 } from 'uuid';
import { Filter } from 'components/resultSearch/filter';
import { FilterEdit } from 'components/resultSearch/filterEdit';

import hash from 'object-hash';
import { Ordered, orderedComparator } from 'components/ordered';
import { determineNotableKeys } from 'components/resultSearch/jsonSchema';
import Flex from 'components/flex';
import qs from 'qs';
import { SiteSearchPopover } from 'components/searchSelectors/siteSearchPopover';
import { BenchmarkSearchSelect } from 'components/searchSelectors/benchmarkSearchSelect';
import { FlavorSearchSelect } from 'components/searchSelectors/flavorSearchSelect';

type QueryParams = {
    benchmarkId?: string;
    siteId?: string;
    flavorId?: string;
};

function ResultSearch(): ReactElement {
    const [queryParams, setQueryParams] = useState<QueryParams>(
        qs.parse(window.location.search.slice(1))
    );
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

    const suggestedFields = benchmark ? determineNotableKeys(benchmark) : undefined;

    const [resultsPerPage, setResultsPerPage_] = useState(20);
    const [page, setPage] = useState(1);
    // json preview modal
    const [showJSONPreview, setShowJSONPreview] = useState(false);

    const [showReportModal, setShowReportModal] = useState(false);

    const [selectedResults, setSelectedResults] = useState<Ordered<Result>[]>([]);

    const [previewResult, setPreviewResult] = useState<Result | null>(null);
    const [reportedResult, setReportedResult] = useState<Result | null>(null);

    function setResultsPerPage(results: number) {
        setResultsPerPage_(results);
        setPage(1);
    }

    // helpers for subelements
    const resultOps = {
        select: function (result: Ordered<Result>) {
            if (!this.isSelected(result)) {
                // cannot call setSelectedResults directly, need to put in variable first
                const arr = [...selectedResults, result].sort(orderedComparator);
                setSelectedResults(arr);
            }
        },
        selectMultiple: function (results: Ordered<Result>[]) {
            const newResults = results.filter((r) => !resultOps.isSelected(r));
            if (newResults.length === 0) {
                return;
            }
            const combined = [...selectedResults, ...newResults].sort(orderedComparator);
            setSelectedResults(combined);
        },
        unselect: function (result: Result) {
            setSelectedResults(selectedResults.filter((r) => r.id !== result.id));
        },
        unselectMultiple: function (results: Result[]) {
            setSelectedResults(
                selectedResults.filter(
                    (selected) => !results.some((unselected) => unselected.id === selected.id)
                )
            );
        },
        isSelected: function (result: Result) {
            return selectedResults.some((r) => r.id === result.id);
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
                        if (
                            filter === undefined ||
                            filter.key.length === 0 ||
                            filter.value.length === 0
                        ) {
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
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    function refreshLocation(queryParams: QueryParams) {
        window.history.replaceState(
            null,
            '',
            window.location.pathname +
                qs.stringify(queryParams, {
                    addQueryPrefix: true,
                })
        );
    }

    function updateBenchmark(benchmark?: Benchmark) {
        setBenchmark(benchmark);
        const newQueryParams = {
            ...queryParams,
            benchmarkId: benchmark?.id,
        };
        refreshLocation(newQueryParams);
        setQueryParams(newQueryParams);

        setSelectedResults([]);
    }

    function updateSite(site?: Site) {
        setSite(site);
        const newQueryParams = {
            ...queryParams,
            siteId: site?.id,
        };
        refreshLocation(newQueryParams);
        setQueryParams(newQueryParams);
    }

    function updateFlavor(flavor?: Flavor) {
        setFlavor(flavor);
        const newQueryParams = {
            ...queryParams,
            flavorId: flavor?.id,
        };
        refreshLocation(newQueryParams);
        setQueryParams(newQueryParams);
    }

    return (
        <>
            <Container fluid="xl">
                <Row className="mb-2">
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
                                        <BenchmarkSearchSelect
                                            benchmark={benchmark}
                                            setBenchmark={updateBenchmark}
                                            initialBenchmarkId={queryParams.benchmarkId}
                                        />
                                        <SiteSearchPopover
                                            site={site}
                                            setSite={updateSite}
                                            initialSiteId={queryParams.siteId}
                                        />
                                        <FlavorSearchSelect
                                            site={site}
                                            flavor={flavor}
                                            setFlavor={updateFlavor}
                                            initialFlavorId={queryParams.flavorId}
                                        />
                                        <hr />
                                        <ListGroup variant="flush">
                                            {[...filters.keys()].flatMap((key) => {
                                                const filter = filters.get(key);
                                                if (filter === undefined) {
                                                    return [];
                                                }

                                                return [
                                                    <ListGroup.Item key={key}>
                                                        <FilterEdit
                                                            filter={filter}
                                                            setFilter={setFilter}
                                                            deleteFilter={deleteFilter}
                                                            suggestions={suggestedFields}
                                                        />
                                                    </ListGroup.Item>,
                                                ];
                                            })}
                                        </ListGroup>
                                        <Flex>
                                            <Flex.FloatLeft>
                                                <Button variant="success" onClick={addFilter}>
                                                    Add filter
                                                </Button>
                                            </Flex.FloatLeft>
                                            <Flex.FloatRight className="d-flex">
                                                <Button onClick={() => results.refetch()}>
                                                    Apply filters
                                                </Button>
                                            </Flex.FloatRight>
                                        </Flex>
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
                <Card>
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
                        <Flex className="m-2">
                            <Flex.FloatLeft>
                                <ResultsPerPageSelection
                                    onChange={setResultsPerPage}
                                    currentSelection={resultsPerPage}
                                />
                            </Flex.FloatLeft>
                            <Flex.Center className="d-flex">
                                <Paginator pagination={results.data.data} navigateTo={setPage} />
                            </Flex.Center>
                            <Flex.FloatRight className="d-flex" />
                        </Flex>
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

const ResultSearchPage: Page = {
    path: '/result-search',
    component: ResultSearch,
    name: 'ResultSearch',
    displayName: 'Search',
};

export default ResultSearchPage;
