import React, { ReactElement, useState } from 'react';
import { Accordion, Button, Card, Col, Container, ListGroup, Row } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { useQuery } from 'react-query';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { ResultsPerPageSelection } from 'components/resultsPerPageSelection';
import { CardAccordionToggle } from 'components/cardAccordionToggle';
import { getHelper } from 'components/api-helpers';
import { ResultTable } from 'components/resultSearch/resultTable';
import { Benchmark, Flavor, Result, Results, Site } from 'model';
import { Paginator } from 'components/pagination';
import { DiagramView } from 'components/resultSearch/diagramView';
import { ResultReportModal } from 'components/resultReportModal';
import { v4 as uuidv4 } from 'uuid';
import { Filter } from 'components/resultSearch/filter';
import { FilterEdit } from 'components/resultSearch/filterEdit';

import { Ordered, orderedComparator } from 'components/ordered';
import { determineNotableKeys } from 'components/resultSearch/jsonSchema';
import Flex from 'components/flex';
import { SiteSearchPopover } from 'components/searchSelectors/siteSearchPopover';
import { BenchmarkSearchSelect } from 'components/searchSelectors/benchmarkSearchSelect';
import { FlavorSearchSelect } from 'components/searchSelectors/flavorSearchSelect';
import { Sorting, SortMode } from 'components/resultSearch/sorting';
import { useRouter } from 'next/router';

/**
 * Search page for ran benchmarks
 * @returns {React.ReactElement}
 * @constructor
 */
function ResultSearch(): ReactElement {
    const router = useRouter();

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);

    const [filters, setFilters] = useState<Map<string, Filter>>(new Map());

    const [sorting, setSorting] = useState<Sorting>({
        mode: SortMode.Disabled,
        key: ''
    });

    function addFilter() {
        const newMap = new Map(filters); // shallow copy
        const id = uuidv4();
        newMap.set(id, {
            id,
            key: '',
            mode: '>',
            value: ''
        });
        setFilters(newMap);
    }

    function setFilter(id: string, key: string, mode: string, value: string) {
        const newMap = new Map(filters); // shallow copy
        newMap.set(id, {
            id,
            key,
            mode,
            value
        });
        setFilters(newMap);
    }

    function deleteFilter(id: string) {
        const newMap = new Map(filters); // shallow copy
        newMap.delete(id);
        setFilters(newMap);
    }

    const suggestedFields = benchmark
        ? determineNotableKeys(benchmark)
        : undefined;

    const [resultsPerPage, setResultsPerPage_] = useState(20);
    const [page, setPage] = useState(1);
    // json preview modal
    const [showJSONPreview, setShowJSONPreview] = useState(false);

    const [showReportModal, setShowReportModal] = useState(false);

    const [selectedResults, setSelectedResults] = useState<Ordered<Result>[]>([]);

    const [previewResult, setPreviewResult] = useState<Result | null>(null);
    const [reportedResult, setReportedResult] = useState<Result | null>(null);

    //
    const [customColumns, setCustomColumns] = useState<string[]>([]);

    function setResultsPerPage(results: number) {
        setResultsPerPage_(results);
        setPage(1);
    }

    // helpers for subelements
    const resultOps = {
        select: function(result: Ordered<Result>) {
            if (!this.isSelected(result)) {
                // cannot call setSelectedResults directly, need to put in variable first
                const arr = [...selectedResults, result].sort(orderedComparator);
                setSelectedResults(arr);
            }
        },
        selectMultiple: function(results: Ordered<Result>[]) {
            const newResults = results.filter((r) => !resultOps.isSelected(r));
            if (newResults.length === 0) {
                return;
            }
            const combined = [...selectedResults, ...newResults].sort(
                orderedComparator
            );
            setSelectedResults(combined);
        },
        unselect: function(result: Result) {
            setSelectedResults(selectedResults.filter((r) => r.id !== result.id));
        },
        unselectMultiple: function(results: Result[]) {
            setSelectedResults(
                selectedResults.filter(
                    (selected) =>
                        !results.some((unselected) => unselected.id === selected.id)
                )
            );
        },
        isSelected: function(result: Result) {
            return selectedResults.some((r) => r.id === result.id);
        },
        display: function(result: Result) {
            setPreviewResult(result);
            setShowJSONPreview(true);
        },
        report: function(result: Result) {
            setReportedResult(result);
            setShowReportModal(true);
        }
    };

    // hash used for queryKey to not have to add a dozen strings
    const results = useQuery(
        [
            'results',
            resultsPerPage,
            page,
            benchmark?.id,
            site?.id,
            site !== undefined ? flavor?.id : undefined,
            sorting.mode === SortMode.Ascending
                ? '+' + sorting.key
                : sorting.mode === SortMode.Descending
                    ? '-' + sorting.key
                    : undefined
        ],
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
                sort_by:
                    sorting.mode === SortMode.Ascending
                        ? '+' + sorting.key
                        : sorting.mode === SortMode.Descending
                            ? '-' + sorting.key
                            : undefined
            });
        },
        {
            refetchOnWindowFocus: false // do not spam queries
        }
    );

    function refreshLocation(benchmark: Benchmark | undefined, site: Site | undefined, flavor: Flavor | undefined) {
        let query = {};
        if (benchmark && benchmark.id) {
            query = { ...query, benchmarkId: benchmark.id };
        }
        if (site && site.id) {
            query = { ...query, siteId: site.id };
        }
        if (flavor && flavor.id) {
            query = { ...query, flavorId: flavor.id };
        }
        router.push({
            pathname: '/search/result',
            query
        }, undefined, { shallow: true });
    }

    function updateBenchmark(benchmark?: Benchmark) {
        setBenchmark(benchmark);
        setSelectedResults([]);

        refreshLocation(benchmark, site, flavor);
    }

    function updateSite(site?: Site) {
        setSite(site);
        setFlavor(undefined);

        refreshLocation(benchmark, site, flavor);
    }

    function updateFlavor(flavor?: Flavor) {
        setFlavor(flavor);

        refreshLocation(benchmark, site, flavor);
    }

    return (
        <>
            <Container fluid='xl'>
                <Row className='mb-2'>
                    <Col>
                        <Accordion defaultActiveKey='filters'>
                            <Card>
                                <Card.Header>
                                    <CardAccordionToggle eventKey='filters'>
                                        Filters
                                    </CardAccordionToggle>
                                </Card.Header>
                                <Accordion.Collapse eventKey='filters'>
                                    <Card.Body>
                                        {router.isReady && <>
                                            <BenchmarkSearchSelect
                                                benchmark={benchmark}
                                                initBenchmark={(b) => setBenchmark(b)}
                                                setBenchmark={updateBenchmark}
                                                initialBenchmarkId={router.query.benchmarkId as string | undefined}
                                            />
                                            <SiteSearchPopover
                                                site={site}
                                                initSite={(s) => setSite(s)}
                                                setSite={updateSite}
                                                initialSiteId={router.query.siteId as string | undefined}
                                            />
                                            <FlavorSearchSelect
                                                site={site}
                                                flavor={flavor}
                                                initFlavor={(f) => setFlavor(f)}
                                                setFlavor={updateFlavor}
                                                initialFlavorId={router.query.flavorId as string | undefined}
                                            />
                                        </>}
                                        <hr />
                                        <ListGroup variant='flush'>
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
                                                    </ListGroup.Item>
                                                ];
                                            })}
                                        </ListGroup>
                                        <Flex>
                                            <Flex.FloatLeft>
                                                <Button variant='success' onClick={addFilter}>
                                                    Add filter
                                                </Button>
                                            </Flex.FloatLeft>
                                            <Flex.FloatRight className='d-flex'>
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
                        <Accordion defaultActiveKey='diagram'>
                            <Card>
                                <Card.Header>
                                    <CardAccordionToggle eventKey='diagram'>
                                        Comparison diagram
                                    </CardAccordionToggle>
                                </Card.Header>
                                <Accordion.Collapse eventKey='diagram'>
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
                                sorting={sorting}
                                setSorting={(sort) => {
                                    setSorting(sort);
                                }}
                                customColumns={customColumns}
                                setCustomColumns={setCustomColumns}
                            />
                        )}
                        {results.isSuccess && results.data.data.total === 0 && (
                            <div className='text-muted m-2'>No results found! :(</div>
                        )}
                        {results.isError && 'Error while loading results'}
                        {results.isLoading && <LoadingOverlay />}
                    </div>
                    {/* fuck flexbox & CSS spacing */}
                    {results.isSuccess && (
                        <Flex className='m-2'>
                            <Flex.FloatLeft>
                                <ResultsPerPageSelection
                                    onChange={setResultsPerPage}
                                    currentSelection={resultsPerPage}
                                />
                            </Flex.FloatLeft>
                            <Flex.Center className='d-flex'>
                                <Paginator
                                    pagination={results.data.data}
                                    navigateTo={setPage}
                                />
                            </Flex.Center>
                            <Flex.FloatRight className='d-flex' />
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

export default ResultSearch;
