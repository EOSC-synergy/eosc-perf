import React, { ReactElement, ReactNode, useState } from 'react';
import { useQuery } from 'react-query';
import { SearchForm } from './searchForm';
import { Table } from './table';
import { LoadingOverlay } from '../loadingOverlay';
import { getHelper } from 'api-helpers';
import { Paginated, Paginator } from '../pagination';
import { Button, Col, OverlayTrigger, Popover, Row } from 'react-bootstrap';
import { Identifiable } from '../identifiable';

export function SimpleSearchPopover<Item extends Identifiable>(props: {
    queryKeyPrefix: string;
    tableName: string;
    endpoint: string;
    item?: Item;
    setItem: (item?: Item) => void;
    display: (item?: Item) => ReactNode;
    displayRow: (item: Item) => ReactNode;
    submitNew?: () => void;
}): ReactElement {
    //const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);

    const [searchString, setSearchString] = useState<string>('');

    const items = useQuery(
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
                                setItem={() => undefined}
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
                            items={items.data.data.items}
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
        <div className="my-1">
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
