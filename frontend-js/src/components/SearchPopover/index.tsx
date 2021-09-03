import React, { ReactNode, useState } from 'react';
import { useQuery } from 'react-query';
import { SearchForm } from './searchForm';
import { Table } from './table';
import { LoadingOverlay } from '../loadingOverlay';
import { Benchmark, Flavor, Site } from 'api';
import { getHelper } from 'api-helpers';
import { Paginated, Paginator } from '../pagination';
import { Button, Col, OverlayTrigger, Popover, Row } from 'react-bootstrap';
import { Identifiable } from '../identifiable';
import { BenchmarkSubmissionModal } from '../benchmarkSubmissionModal';
import { SiteSubmissionModal } from '../siteSubmissionModal';
import { FlavorSubmissionModal } from '../flavorSubmissionModal';

function SimpleSearchPopover<Item extends Identifiable>(props: {
    queryKeyPrefix: string;
    tableName: string;
    endpoint: string;
    item?: Item;
    setItem: (item?: Item) => void;
    display: (item?: Item) => ReactNode;
    displayRow: (item: Item) => ReactNode;
    submitNew?: () => void;
}) {
    //const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);

    const [searchString, setSearchString] = useState<string>('');

    let items = useQuery(
        props.queryKeyPrefix + '-page-' + page + '-' + searchString,
        () => {
            return getHelper<Paginated<Item>>(props.endpoint, undefined, {
                // split here so we can add searchString to key to fetch automatically
                terms: searchString.split(' '),
            });
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const popover = (
        <Popover id="benchmarkSelect" style={{ maxWidth: '576px', width: 'auto' }}>
            <Popover.Header as="h3">Benchmark Search</Popover.Header>
            <Popover.Body>
                <SearchForm setSearchString={setSearchString} />
                <div style={{ position: 'relative' }}>
                    {items.isLoading && (
                        <>
                            <Table<Item>
                                setItem={() => {}}
                                items={[]}
                                tableName={props.tableName}
                                displayItem={() => {
                                    return <></>;
                                }}
                            />
                            <LoadingOverlay />
                        </>
                    )}
                    {items.isError && <div>Failed to fetch benchmarks!</div>}
                    {items.isSuccess && (
                        <Table<Item>
                            items={items.data.data.items!}
                            setItem={props.setItem}
                            tableName={props.tableName}
                            displayItem={props.displayRow}
                        />
                    )}
                </div>
                <Row>
                    {items.isSuccess && (
                        <Col>
                            <Paginator pagination={items.data.data} navigateTo={setPage} />
                        </Col>
                    )}
                    <Col md="auto">
                        <Button
                            className="m-1"
                            variant="secondary"
                            onClick={() => props.setItem(undefined)}
                        >
                            Deselect
                        </Button>
                        {/* TODO: hide popover if submit button is pressed */}
                        {props.submitNew && (
                            <Button className="m-1" onClick={props.submitNew}>
                                + New
                            </Button>
                        )}
                    </Col>
                </Row>
            </Popover.Body>
        </Popover>
    );

    return (
        <div className="m-1">
            <Row>
                <Col>{props.display(props.item)} </Col>
                <Col md="auto">
                    <OverlayTrigger trigger="click" placement="bottom" overlay={popover} rootClose>
                        <Button variant="success" size="sm">
                            Select
                        </Button>
                    </OverlayTrigger>
                </Col>
            </Row>
        </div>
    );
}

export function BenchmarkSearchPopover(props: {
    benchmark?: Benchmark;
    setBenchmark: (benchmark?: Benchmark) => void;
}) {
    function display(benchmark?: Benchmark) {
        return (
            <>
                Benchmark:{' '}
                {benchmark ? (
                    <a href={'https://hub.docker.com/repository/docker/' + benchmark.docker_image}>
                        {benchmark.docker_image + ':' + benchmark.docker_tag}
                    </a>
                ) : (
                    <div className="text-muted" style={{ display: 'inline-block' }}>
                        None
                    </div>
                )}
            </>
        );
    }

    function displayRow(benchmark: Benchmark) {
        return (
            <>
                <a
                    title={benchmark.docker_image + ':' + benchmark.docker_tag}
                    href="#"
                    onClick={() => props.setBenchmark(benchmark)}
                >
                    {benchmark.docker_image + ':' + benchmark.docker_tag}
                </a>
                <div>
                    {benchmark.description}
                    <br />
                </div>
            </>
        );
    }

    const [showSubmitModal, setShowSubmitModal] = useState(false);

    return (
        <>
            <SimpleSearchPopover<Benchmark>
                queryKeyPrefix="benchmark"
                tableName="Benchmark"
                endpoint="/benchmarks/search"
                item={props.benchmark}
                setItem={props.setBenchmark}
                display={display}
                displayRow={displayRow}
                submitNew={() => setShowSubmitModal(true)}
            />
            <BenchmarkSubmissionModal
                show={showSubmitModal}
                onHide={() => setShowSubmitModal(false)}
            />
        </>
    );
}

export function SiteSearchPopover(props: { site?: Site; setSite: (site?: Site) => void }) {
    function display(site?: Site) {
        return (
            <>
                Site:{' '}
                {site ? (
                    <>{site.name}</>
                ) : (
                    <div className="text-muted" style={{ display: 'inline-block' }}>
                        None
                    </div>
                )}
            </>
        );
    }

    function displayRow(site: Site) {
        return (
            <>
                <a title={site.name} href="#" onClick={() => props.setSite(site)}>
                    {site.name}
                </a>
                <div>
                    {site.description}
                    <br />
                </div>
            </>
        );
    }

    const [showSubmitModal, setShowSubmitModal] = useState(false);

    return (
        <>
            <SimpleSearchPopover<Site>
                queryKeyPrefix="site"
                tableName="Site"
                endpoint="/sites/search"
                item={props.site}
                setItem={props.setSite}
                display={display}
                displayRow={displayRow}
                submitNew={() => setShowSubmitModal(true)}
            />
            <SiteSubmissionModal show={showSubmitModal} onHide={() => setShowSubmitModal(false)} />
        </>
    );
}

export function FlavorSearchPopover(props: {
    site?: Site;
    flavor?: Flavor;
    setFlavor: (flavor?: Flavor) => void;
}) {
    function display(flavor?: Flavor) {
        return (
            <>
                Flavor:{' '}
                {flavor ? (
                    <>{flavor.name}</>
                ) : (
                    <div className="text-muted" style={{ display: 'inline-block' }}>
                        None
                    </div>
                )}
            </>
        );
    }

    function displayRow(flavor: Flavor) {
        return (
            <>
                <a title={flavor.name} href="#" onClick={() => props.setFlavor(flavor)}>
                    {flavor.name}
                </a>
                <div>
                    {flavor.description}
                    <br />
                </div>
            </>
        );
    }

    const [showSubmitModal, setShowSubmitModal] = useState(false);

    return (
        <>
            {props.site ? (
                <>
                    <SimpleSearchPopover<Flavor>
                        queryKeyPrefix={'flavor-for-' + props.site.id}
                        tableName="Flavor"
                        endpoint={'/sites/' + props.site.id + '/flavors/search'}
                        item={props.flavor}
                        setItem={props.setFlavor}
                        display={display}
                        displayRow={displayRow}
                        submitNew={() => setShowSubmitModal(true)}
                    />
                    <FlavorSubmissionModal
                        show={showSubmitModal}
                        onHide={() => setShowSubmitModal(false)}
                        site={props.site}
                    />
                </>
            ) : (
                <></>
            )}
        </>
    );
}
