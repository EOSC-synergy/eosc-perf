import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Benchmark, Result, Site } from 'model';
import { Alert, Badge, Col, Form, Row } from 'react-bootstrap';
import { Ordered } from 'components/ordered';
import { Suggestion } from '../jsonSchema';
import {
    DataPoint,
    DataPointCollection,
    generateDataPoints,
    RejectedResult,
    XAxis,
    YAxis,
} from './helpers';

import ReactEChartsCore from 'echarts-for-react/lib/core';
import * as echarts from 'echarts/core';
import { ScatterChart, LineChart, BarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, DatasetComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// TODO: remove ts ignore if this gets ever fixed
// @ts-ignore
import { transform } from 'echarts-stat';
import { getSubkeyName } from '../jsonKeyHelpers';

echarts.use([
    TooltipComponent,
    GridComponent,
    ScatterChart,
    CanvasRenderer,
    LineChart,
    DatasetComponent,
    BarChart,
]);
echarts.registerTransform(transform.regression);

enum Scale {
    Linear,
    Logarithmic,
}

enum GraphMode {
    Scatter = 'scatter',
    Line = 'line',
    Bar = 'bar',
}

enum Regression {
    None = '',
    Linear = 'linear',
    Exponential = 'exponential',
    Logarithmic = 'logarithmic',
    Polynomial = 'polynomial',
}

function RegressionSelect(props: {
    setRegressionMode: (mode: string) => void;
    regressionMode: string;
    disabled: boolean;
    polyRegressionOrder: number;
    setPolyRegressionOrder: (num: number) => void;
}) {
    return (
        <Form.Group>
            <Row>
                <Col sm="auto" className="align-self-center">
                    <Form.Label style={{ marginBottom: 0 }}>Regression</Form.Label>
                </Col>
                <Col>
                    {props.disabled || (
                        <Form.Select
                            onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                                props.setRegressionMode(e.target.value);
                            }}
                            size="sm"
                            value={props.regressionMode}
                            disabled={props.disabled}
                        >
                            <option value={Regression.None} />
                            <option value={Regression.Linear}>Linear</option>
                            <option value={Regression.Exponential}>Exponential</option>
                            <option value={Regression.Polynomial}>Polynomial</option>
                            <option value={Regression.Logarithmic}>Logarithmic</option>
                        </Form.Select>
                    )}
                    {props.disabled && (
                        <Badge bg="secondary">All results must be from same site</Badge>
                    )}
                </Col>
                {props.regressionMode === Regression.Polynomial && (
                    <Col md="auto">
                        <Form.Select
                            onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                                props.setPolyRegressionOrder(parseInt(e.target.value));
                            }}
                            size="sm"
                            value={props.polyRegressionOrder}
                            disabled={props.regressionMode !== Regression.Polynomial}
                        >
                            {/* 1 - 10 */}
                            {[...Array(10).keys()].map((n) => (
                                <option value={n + 1} key={n + 1}>
                                    {n + 1}
                                </option>
                            ))}
                        </Form.Select>
                    </Col>
                )}
            </Row>
        </Form.Group>
    );
}

function GraphModeSelect(props: { setGraphMode: (value: string) => void; graphMode: string }) {
    return (
        <Form.Group>
            <Row>
                <Col sm="auto" className="align-self-center">
                    <Form.Label style={{ marginBottom: 0 }}>Graph mode</Form.Label>
                </Col>
                <Col>
                    <Form.Select
                        onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                            props.setGraphMode(e.target.value);
                        }}
                        size="sm"
                        value={props.graphMode}
                    >
                        <option value={GraphMode.Scatter}>Scatter</option>
                        <option value={GraphMode.Line}>Line</option>
                        <option value={GraphMode.Bar}>Bar</option>
                    </Form.Select>
                </Col>
            </Row>
        </Form.Group>
    );
}

function XAxisModeSelect(props: { setXAxisMode: (value: Scale) => void; xAxisMode: Scale }) {
    return (
        <Form.Group className="my-1">
            <Row>
                <Col sm="auto" className="align-self-center">
                    <Form.Label style={{ marginBottom: 0 }}>X Scale</Form.Label>
                </Col>
                <Col>
                    <Form.Select
                        onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                            props.setXAxisMode(parseInt(e.target.value));
                        }}
                        size="sm"
                        value={props.xAxisMode}
                    >
                        <option value={Scale.Linear}>Linear</option>
                        <option value={Scale.Logarithmic}>Logarithmic</option>
                    </Form.Select>
                </Col>
            </Row>
        </Form.Group>
    );
}

function YAxisModeSelect(props: { setYAxisMode: (value: Scale) => void; yAxisMode: Scale }) {
    return (
        <Form.Group className="my-1">
            <Row>
                <Col sm="auto" className="align-self-center">
                    <Form.Label style={{ marginBottom: 0 }}>Y Scale</Form.Label>
                </Col>
                <Col>
                    <Form.Select
                        onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                            props.setYAxisMode(parseInt(e.target.value));
                        }}
                        size="sm"
                        value={props.yAxisMode}
                    >
                        <option value={Scale.Linear}>Linear</option>
                        <option value={Scale.Logarithmic}>Logarithmic</option>
                    </Form.Select>
                </Col>
            </Row>
        </Form.Group>
    );
}

/**
 * Chart displaying a line diagram following the results' ordering
 * @param {Ordered<Result>[]} results
 * @param {string[]} suggestions List of diagram keys to suggest to user for axes
 * @param {Benchmark} benchmark
 * @returns {React.ReactElement}
 * @constructor
 */
function EChartsDiagram({
    results,
    suggestions,
    benchmark,
}: {
    results: Ordered<Result>[];
    suggestions?: Suggestion[];
    benchmark?: Benchmark;
}): ReactElement {
    const [xAxisMode, setXAxisMode] = useState(Scale.Linear);
    const [yAxisMode, setYAxisMode] = useState(Scale.Linear);

    const [graphMode, setGraphMode] = useState<string>(GraphMode.Line);
    const [regressionMode, setRegressionMode] = useState<string>(Regression.None);
    const [polyRegressionOrder, setPolyRegressionOrder] = useState<number>(2);

    const [xAxis, setXAxis] = useState('');
    const [yAxis, setYAxis] = useState('');

    const labelSet = new Set<number>();

    let dataPoints: DataPointCollection = new Map<string, { site: Site; data: DataPoint[] }>();
    let rejected: RejectedResult[] = [];
    let siteCount = 0;

    // if axes entered, parse data by x and y
    if (xAxis.length && yAxis.length) {
        [dataPoints, rejected] = generateDataPoints(results, xAxis, yAxis);
        for (const site of dataPoints.values()) {
            for (const dataPoint of site.data) {
                labelSet.add(dataPoint.x);
            }
            siteCount++;
        }
    }

    let datasets: ({ source: number[][] } | { transform: unknown })[] = [];
    let series = [];
    for (const dataSet of dataPoints.values()) {
        datasets.push({ source: dataSet.data.map((d) => [d.x, d.y]) });
        series.push({
            type: graphMode,
            name: dataSet.site.name,
            datasetIndex: datasets.length - 1,
        });
    }

    const regressionDataset = {
        transform: {
            type: 'ecStat:regression',
            config: {
                method: regressionMode,
                // 'end' by default
                // formulaOn: 'start'
                order: polyRegressionOrder,
            },
        },
    };
    const regressionSeries = {
        name: 'Regression',
        type: 'line',
        smooth: true,
        datasetIndex: datasets.length,
        symbolSize: 0.1,
        symbol: 'circle',
        label: { show: true, fontSize: 16 },
        labelLayout: {
            rotate: 0,
            x: '15%',
            y: '010%',
            fontSize: 12,
        },
        encode: { label: 2, tooltip: 1 },
    };

    // TODO: BUG: cannot deselect regression (will also apply if disabled because more sites
    const enableRegression = regressionMode !== Regression.None && siteCount === 1;
    if (enableRegression) {
        datasets.push(regressionDataset);
        series.push(regressionSeries);
    }

    const options = {
        dataset: [...datasets],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
            },
        },
        xAxis: {
            splitLine: {
                lineStyle: {
                    type: 'dashed',
                },
            },
            type: xAxisMode === Scale.Logarithmic ? 'log' : 'value',
            name: getSubkeyName(xAxis),
        },
        yAxis: {
            splitLine: {
                lineStyle: {
                    type: 'dashed',
                },
            },
            type: yAxisMode === Scale.Logarithmic ? 'log' : 'value',
            name: getSubkeyName(yAxis),
            nameRotate: 90,
        },
        series: [...series],
        animation: false,
    };

    return (
        <>
            <GraphModeSelect setGraphMode={setGraphMode} graphMode={graphMode} />
            <Row>
                <Col>
                    <XAxisModeSelect setXAxisMode={setXAxisMode} xAxisMode={xAxisMode} />
                </Col>
                <Col>
                    <YAxisModeSelect setYAxisMode={setYAxisMode} yAxisMode={yAxisMode} />
                </Col>
            </Row>
            <RegressionSelect
                setRegressionMode={setRegressionMode}
                regressionMode={regressionMode}
                polyRegressionOrder={polyRegressionOrder}
                setPolyRegressionOrder={setPolyRegressionOrder}
                disabled={siteCount !== 1}
            />
            <XAxis setXAxis={setXAxis} suggestions={suggestions} />
            <YAxis setYAxis={setYAxis} suggestions={suggestions} />

            {rejected.length > 0 && (
                <div className="my-1">
                    {datasets.length > 0 &&
                        rejected.map((rejected) => (
                            <Alert variant="warning" key={rejected.result.id}>
                                Result {rejected.result.id} not displayed due to: {rejected.reason}
                            </Alert>
                        ))}
                    {datasets.length === 0 && (
                        <Alert variant="danger">
                            No displayable result selected. One of your axes may not be referencing
                            numeric data!
                        </Alert>
                    )}
                </div>
            )}
            {xAxis.length > 0 && yAxis.length > 0 && datasets.length > 0 && (
                <ReactEChartsCore echarts={echarts} option={options} />
            )}

            {/* TODO: download png / csv buttons */}
        </>
    );
}

const EChartsMeta = {
    element: EChartsDiagram,
    name: 'Apache ECharts',
    id: 'apache-echarts',
};

export default EChartsMeta;
