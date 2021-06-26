import React, { useEffect, useState } from 'react';
import { Accordion, Button, Card, Container } from 'react-bootstrap';
import { LoadingOverlay } from '../loadingOverlay';
import { useQuery } from 'react-query';
import axios from 'axios';
import { ColumnSelectModal } from './columnSelectModal';
import { JSONPreviewModal } from './JSONPreviewModal';
import { ResultsPerPageSelection } from './resultsPerPageSelection';
import { NumberedPagination } from './numberedPagination';
import { BenchmarkSelection } from './benchmarkSelection';
import { CardAccordionToggle } from './cardAccordionToggle';
import { Result } from '../../api';
import { getHelper } from '../../api-helpers';

const qs = require('qs');

type ResultSearchProps = {
    initialBenchmark: string;
    location: { search: string };
    token: string;
};

function ResultSearch(props: ResultSearchProps) {
    const [benchmark, setBenchmark] = useState(qs.parse(props.location.search).benchmark || '');

    const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);
    // json preview modal
    const [showJSONPreview, setShowJSONPreview] = useState(false);
    // column selection modal
    const [showColumnSelection, setShowColumnSelection] = useState(false);

    // put token in state
    const [token, setToken] = useState(props.token);
    // propagate props to state for token update
    useEffect(() => {
        setToken(props.token);
    }, [props.token]);

    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'benchmarkSearch',
        () => {
            return getHelper<Result[]>('/api/results', props.token);
        },
        {
            enabled: !!token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    function Search() {
        // TODO
    }

    function AddFilter() {
        // TODO
    }

    // separate accordions to allow each element to be open simultaneously

    return (
        <div className="container-fluid">
            <Container>
                <h1>Result Search</h1>
                <Accordion defaultActiveKey="filters">
                    <Card>
                        <Card.Header>
                            <CardAccordionToggle eventKey="filters">Filters</CardAccordionToggle>
                        </Card.Header>
                        <Accordion.Collapse eventKey="filters">
                            <Card.Body>
                                <BenchmarkSelection onChange={setBenchmark} benchmark={benchmark} />
                                <hr />
                                {/* TODO: Filters wrapper */}
                                <ul id="filters" className="list-unstyled d-flex flex-column"></ul>
                                <Button variant="primary" onSubmit={Search}>
                                    Search
                                </Button>
                                <Button variant="success" onSubmit={AddFilter}>
                                    Add Filter
                                </Button>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
                <Accordion defaultActiveKey="diagram">
                    <Card>
                        <Card.Header>
                            <CardAccordionToggle eventKey="diagram">
                                Comparison diagram
                            </CardAccordionToggle>
                        </Card.Header>
                        <Accordion.Collapse eventKey="diagram">
                            <Card.Body>
                                <div className="form-inline">
                                    <label htmlFor="diagramDropdown">Select diagram type:</label>
                                    <select
                                        name="diagram-choice"
                                        id="diagramDropdown"
                                        onChange={() => {} /*search_page.select_diagram_type()*/}
                                        className="custom-select"
                                        disabled
                                    >
                                        <option value="speedup">Line graph</option>
                                    </select>
                                    <span
                                        className="badge badge-secondary"
                                        id="diagramDropdownBenchmarkHint"
                                    >
                                        Please select a benchmark
                                    </span>
                                </div>
                                <div id="diagramConfiguration-speedup" className="d-none">
                                    <select
                                        className="custom-select"
                                        id="speedupDiagramMode"
                                        onChange={
                                            () => {} /*search_page.update_diagram_configuration()*/
                                        }
                                    >
                                        <option id="speedupDiagramMode-simple" value="simple">
                                            Simple
                                        </option>
                                        <option id="speedupDiagramMode-linear" value="linear">
                                            Linear
                                        </option>
                                        <option id="speedupDiagramMode-log" value="log">
                                            Logarithmic
                                        </option>
                                    </select>
                                    <div className="form-check">
                                        <input
                                            className="form-check-input"
                                            type="checkbox"
                                            value=""
                                            id="speedupDiagramGroupedMode"
                                            onChange={
                                                () => {} /*search_page.update_diagram_configuration()}*/
                                            }
                                        />
                                        <label
                                            className="form-check-label"
                                            htmlFor="speedupDiagramGroupedMode"
                                        >
                                            Group values by site (only in linear & logarithmic mode)
                                        </label>
                                    </div>
                                </div>
                                <div id="diagramSection" className="d-flex flex-column lead" />
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
            </Container>
            <Container fluid>
                <Card>
                    <div style={{ display: 'relative' }}>
                        <table
                            id="result_table"
                            className="table result-table"
                            style={{ overflowX: 'auto', display: 'inline-block' }}
                        />
                        <LoadingOverlay />
                    </div>

                    <nav aria-label="Page navigation">
                        {data && (
                            <NumberedPagination
                                pageCount={/*Math.ceil(data?.data.length / resultsPerPage)*/ 5}
                                currentPage={page}
                                onChange={setResultsPerPage}
                            />
                        )}
                    </nav>
                    <ResultsPerPageSelection
                        onChange={setResultsPerPage}
                        currentSelection={resultsPerPage}
                    />

                    <div>
                        <Button
                            variant="primary"
                            onClick={() => {} /*search_page.make_column_select_prompt()*/}
                        >
                            Select Columns
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {} /*search_page.selection_invert()*/}
                        >
                            Invert Selection
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {} /*search_page.selection_all()*/}
                        >
                            Select All
                        </Button>
                    </div>
                </Card>
            </Container>
            <JSONPreviewModal show={showJSONPreview} closeModal={() => setShowJSONPreview(false)} />
            <ColumnSelectModal
                show={showColumnSelection}
                closeModal={(columns: string[]) => {}}
                columns={[] /* TODO */}
            />
        </div>
    );
}

const ResultSearchModule = {
    path: '/result-search',
    element: ResultSearch,
    name: 'ResultSearch',
    dropdownName: 'Results',
};

export default ResultSearchModule;
