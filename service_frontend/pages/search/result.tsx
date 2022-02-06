import React, { ReactElement, useEffect, useState } from 'react';
import { Button, Card, Col, Container, Row, Stack } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { useQuery } from 'react-query';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { ResultsPerPageSelection } from 'components/resultsPerPageSelection';
import Head from 'next/head';
import { getHelper } from 'components/api-helpers';
import { ResultTable } from 'components/resultSearch/resultTable';
import { Benchmark, Flavor, Result, Results, Site } from 'model';
import { Paginator } from 'components/pagination';
import { DiagramCard } from 'components/resultSearch/diagramCard';
import { ResultReportModal } from 'components/resultReportModal';
import { v4 as uuidv4 } from 'uuid';
import { Filter } from 'components/resultSearch/filter';
import { FilterEdit } from 'components/resultSearch/filterEdit';

import { Ordered, orderedComparator } from 'components/ordered';
import { parseSuggestions } from 'components/resultSearch/jsonSchema';
import { SiteSearchPopover } from 'components/searchSelectors/siteSearchPopover';
import { BenchmarkSearchSelect } from 'components/searchSelectors/benchmarkSearchSelect';
import { FlavorSearchSelect } from 'components/searchSelectors/flavorSearchSelect';
import { Sorting, SortMode } from 'components/resultSearch/sorting';
import { useRouter } from 'next/router';
import { Funnel, Save2 } from 'react-bootstrap-icons';

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

    const [browserLoaded, setBrowserLoaded] = useState<boolean>(false);

    useEffect(() => {
        setBrowserLoaded(true);
    }, []);

    const [sorting, setSorting] = useState<Sorting>({
        mode: SortMode.Disabled,
        key: '',
    });

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

    const suggestedFields = benchmark ? parseSuggestions(benchmark) : undefined;

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
        reload: function () {
            results.refetch();
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
                : undefined,
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
                        : undefined,
            });
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    function refreshLocation(
        benchmark: Benchmark | undefined,
        site: Site | undefined,
        flavor: Flavor | undefined
    ) {
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
        router.push(
            {
                pathname: '/search/result',
                query,
            },
            undefined,
            { shallow: true }
        );
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
            <Head>
                <title>Search</title>
            </Head>
            <Container fluid="xl">
                <Stack gap={2}>
                    <DiagramCard
                        results={selectedResults}
                        benchmark={benchmark}
                        suggestions={suggestedFields}
                    />
                    <Card>
                        <Card.Body>
                            {browserLoaded && router.isReady && (
                                <Stack gap={2}>
                                    <BenchmarkSearchSelect
                                        benchmark={benchmark}
                                        initBenchmark={(b) => setBenchmark(b)}
                                        setBenchmark={updateBenchmark}
                                        initialBenchmarkId={
                                            router.query.benchmarkId as string | undefined
                                        }
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
                                        initialFlavorId={
                                            router.query.flavorId as string | undefined
                                        }
                                    />
                                </Stack>
                            )}
                            <hr />
                            <Stack gap={2}>
                                <Stack gap={1}>
                                    {[...filters.keys()].flatMap((key, index) => {
                                        const filter = filters.get(key);
                                        if (filter === undefined) {
                                            return [];
                                        }

                                        return [
                                            <FilterEdit
                                                key={index}
                                                filter={filter}
                                                setFilter={setFilter}
                                                deleteFilter={deleteFilter}
                                                suggestions={suggestedFields}
                                            />,
                                        ];
                                    })}
                                </Stack>
                                <Row>
                                    <Col />
                                    <Col md="auto">
                                        <Stack direction="horizontal" gap={2}>
                                            <Button
                                                variant="secondary"
                                                disabled={selectedResults.length === 0}
                                            >
                                                <Save2 /> Export
                                            </Button>
                                            <Button variant="success" onClick={addFilter}>
                                                + Add filter
                                            </Button>
                                            <Button
                                                variant="warning"
                                                onClick={() => results.refetch()}
                                            >
                                                <Funnel /> Apply Filters
                                            </Button>
                                        </Stack>
                                    </Col>
                                </Row>
                                <Stack gap={2}>
                                    <div style={{ overflowX: 'auto' }}>
                                        {results.isSuccess &&
                                            results.data &&
                                            results.data.data.total > 0 && (
                                                <ResultTable
                                                    results={results.data.data.items}
                                                    pageOffset={
                                                        results.data.data.per_page *
                                                        results.data.data.page
                                                    }
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
                                            <div className="text-muted m-2">
                                                No results found! :(
                                            </div>
                                        )}
                                        {results.isError && 'Error while loading results'}
                                        {results.isLoading && <LoadingOverlay />}
                                    </div>
                                    {results.isSuccess && (
                                        <Row className="mx-2">
                                            <Col xs={true} sm={7} md={5} xl={4} xxl={3}>
                                                <ResultsPerPageSelection
                                                    onChange={setResultsPerPage}
                                                    currentSelection={resultsPerPage}
                                                />
                                            </Col>
                                            <Col />
                                            <Col sm={true} md="auto">
                                                <Paginator
                                                    pagination={results.data.data}
                                                    navigateTo={setPage}
                                                />
                                            </Col>
                                        </Row>
                                    )}
                                </Stack>
                            </Stack>
                        </Card.Body>
                    </Card>
                </Stack>
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
