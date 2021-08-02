import React, { useEffect, useState } from 'react';
import { Accordion, Button, Card, Container, Table } from 'react-bootstrap';
import { LoadingOverlay } from '../loadingOverlay';
import { useQuery } from 'react-query';
import { ColumnSelectModal } from './columnSelectModal';
import { JSONPreviewModal } from './JSONPreviewModal';
import { ResultsPerPageSelection } from './resultsPerPageSelection';
import { NumberedPagination } from './numberedPagination';
import { BenchmarkSelection } from './benchmarkSelection';
import { CardAccordionToggle } from './cardAccordionToggle';
import { getHelper } from '../../api-helpers';
import { SelectableResult } from './selectableResult';
import { ResultTable } from './resultTable';
import {
    ActionColumn,
    BenchmarkColumn,
    CheckboxColumn,
    SiteColumn,
    SiteFlavorColumn,
    TagsColumn,
} from './column';

const qs = require('qs');

type ResultSearchProps = {
    initialBenchmark: string;
    location: { search: string };
    token: string;
    admin: boolean;
};

function ResultSearch(props: ResultSearchProps) {
    const [benchmark, setBenchmark] = useState(qs.parse(props.location.search).benchmark || '');

    const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);
    // json preview modal
    const [showJSONPreview, setShowJSONPreview] = useState(false);
    // column selection modal
    const [showColumnSelection, setShowColumnSelection] = useState(false);

    function displayJSON(result: SelectableResult) {
        // TODO
    }

    const [columns, setColumns] = useState([
        new CheckboxColumn(),
        new BenchmarkColumn(),
        new SiteColumn(),
        new SiteFlavorColumn(),
        new TagsColumn(),
        new ActionColumn(displayJSON, props.admin),
    ]);

    // put token in state
    const [token, setToken] = useState(props.token);
    // propagate props to state for token update
    useEffect(() => {
        setToken(props.token);
    }, [props.token]);

    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'benchmarkSearch',
        () => {
            return getHelper<SelectableResult[]>('/results', props.token);
        },
        {
            enabled: !!token,
            refetchOnWindowFocus: false, // do not spam queries
            // add "selected" field to results
            // TODO: other way than a 'selected' flag to select results?
            select: (data) => {
                data.data.map((result) => {
                    return { ...result, selected: false };
                });
                return data;
            },
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
            {/* paddingBottom: 0 to avoid odd gap before results */}
            <Container style={{ paddingBottom: 0 }}>
                <h1>Result Search</h1>
                <Accordion defaultActiveKey="filters">
                    <Card className="m-2">
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
                    <Card className="m-2">
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
                        <ResultTable results={data ? data.data : []} columns={columns} />
                        {isLoading && <LoadingOverlay />}
                    </div>
                    <div className="m-2 text-center">
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

                <div className="d-flex justify-content-between flex-row-reverse">
                    <ResultsPerPageSelection
                        onChange={setResultsPerPage}
                        currentSelection={resultsPerPage}
                        className="m-2 align-self-center"
                    />
                    {data && (
                        <NumberedPagination
                            pageCount={/*Math.ceil(data?.data.length / resultsPerPage)*/ 5}
                            currentPage={page}
                            onChange={setResultsPerPage}
                            className="m-2 align-self-center"
                        />
                    )}
                </div>
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