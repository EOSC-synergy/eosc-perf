import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Benchmark, Result, Site } from 'model';
import { Alert, Col, Form, Row } from 'react-bootstrap';
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
import { ScatterChart, LineChart } from 'echarts/charts';
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
]);
echarts.registerTransform(transform.regression);

enum Mode {
    Linear,
    Logarithmic,
}

/**
 * Chart displaying a line diagram following the results' ordering
 * @param {Ordered<Result>[]} results
 * @param {string[]} suggestions List of diagram keys to suggest to user for axes
 * @param {Benchmark} benchmark
 * @returns {React.ReactElement}
 * @constructor
 */
function Scatter({
    results,
    suggestions,
    benchmark,
}: {
    results: Ordered<Result>[];
    suggestions?: Suggestion[];
    benchmark?: Benchmark;
}): ReactElement {
    const [xAxisMode, setXAxisMode] = useState(Mode.Linear);
    const [yAxisMode, setYAxisMode] = useState(Mode.Linear);

    const [xAxis, setXAxis] = useState('');
    const [yAxis, setYAxis] = useState('');

    const labelSet = new Set<number>();

    let dataPoints: DataPointCollection = new Map<string, { site: Site; data: DataPoint[] }>();
    let rejected: RejectedResult[] = [];

    // if axes entered, parse data by x and y
    if (xAxis.length && yAxis.length) {
        [dataPoints, rejected] = generateDataPoints(results, xAxis, yAxis);
        for (const site of dataPoints.values()) {
            for (const dataPoint of site.data) {
                labelSet.add(dataPoint.x);
            }
        }
    }

    let datasets: { source: number[][] }[] = [];
    let series = [];
    for (const dataSet of dataPoints.values()) {
        datasets.push({ source: dataSet.data.map((d) => [d.x, d.y]) });
        series.push({
            type: 'scatter',
            name: dataSet.site.name,
            datasetIndex: datasets.length - 1,
        });
    }

    const options = {
        dataset: [
            ...datasets,
            /*{
                transform: {
                    type: 'ecStat:regression',
                    config: {
                        method: 'exponential',
                        // 'end' by default
                        // formulaOn: 'start'
                    },
                },
            },*/
        ],
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
            type: xAxisMode === Mode.Logarithmic ? 'log' : 'value',
            name: getSubkeyName(xAxis),
        },
        yAxis: {
            splitLine: {
                lineStyle: {
                    type: 'dashed',
                },
            },
            type: yAxisMode === Mode.Logarithmic ? 'log' : 'value',
            name: getSubkeyName(yAxis),
            nameRotate: 90,
        },
        series: [
            ...series,
            /*{
                name: 'line',
                type: 'line',
                smooth: true,
                datasetIndex: datasets.length - 1,
                symbolSize: 0.1,
                symbol: 'circle',
                label: { show: true, fontSize: 16 },
                labelLayout: { dx: -20 },
                encode: { label: 2, tooltip: 1 },
            },*/
        ],
    };

    return (
        <>
            <Row>
                <Col>
                    <Form.Group className="my-1">
                        <Row>
                            <Col sm="auto" className="align-self-center">
                                <Form.Label style={{ marginBottom: 0 }}>X Scale</Form.Label>
                            </Col>
                            <Col>
                                <Form.Select
                                    onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                                        setXAxisMode(parseInt(e.target.value));
                                    }}
                                    size="sm"
                                >
                                    <option value={Mode.Linear}>Linear</option>
                                    <option value={Mode.Logarithmic}>Logarithmic</option>
                                </Form.Select>
                            </Col>
                        </Row>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="my-1">
                        <Row>
                            <Col sm="auto" className="align-self-center">
                                <Form.Label style={{ marginBottom: 0 }}>Y Scale</Form.Label>
                            </Col>
                            <Col>
                                <Form.Select
                                    onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                                        setYAxisMode(parseInt(e.target.value));
                                    }}
                                    size="sm"
                                >
                                    <option value={Mode.Linear}>Linear</option>
                                    <option value={Mode.Logarithmic}>Logarithmic</option>
                                </Form.Select>
                            </Col>
                        </Row>
                    </Form.Group>
                </Col>
            </Row>
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

const ScatterMeta = {
    element: Scatter,
    name: 'Scatter',
    id: 'scatter',
};

export default ScatterMeta;
