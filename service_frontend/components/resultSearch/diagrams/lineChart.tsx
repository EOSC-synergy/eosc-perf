import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Benchmark, Result } from 'model';
import { Alert, Form } from 'react-bootstrap';
import { Line } from 'react-chartjs-2';
import { fetchSubkey, getSubkeyName } from 'components/resultSearch/jsonKeyHelpers';
import { Ordered } from 'components/ordered';
import { InputWithSuggestions } from 'components/inputWithSuggestions';
import {
    CategoryScale,
    Chart as ChartJS,
    ChartData,
    ChartDataset,
    Legend,
    LinearScale,
    LineElement,
    LogarithmicScale,
    PointElement,
    ScatterDataPoint,
    Title,
    Tooltip,
    TooltipItem,
} from 'chart.js';
import { Suggestion } from '../jsonSchema';

ChartJS.register(
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    LineElement,
    Title,
    Tooltip,
    Legend,
    PointElement
);

enum Mode {
    Simple,
    Linear,
    Logarithmic,
}

const CHART_COLORS = [
    'rgb(255, 99, 132)', // red
    'rgb(255, 159, 64)', // orange
    'rgb(255, 205, 86)', // yellow
    'rgb(75, 192, 192)', // green
    'rgb(54, 162, 235)', // blue
    'rgb(153, 102, 255)', // purple
    'rgb(201, 203, 207)', // gray
];

const BACKGROUND_COLORS = [
    'rgba(255, 99, 132, 0.5)', // red
    'rgba(255, 159, 64, 0.5)', // orange
    'rgba(255, 205, 86, 0.5)', // yellow
    'rgba(75, 192, 192, 0.5)', // green
    'rgba(54, 162, 235, 0.5)', // blue
    'rgba(153, 102, 255, 0.5)', // purple
    'rgba(201, 203, 207, 0.5)', // gray
];

/**
 * Chart displaying a line diagram following the results' ordering
 * @param {Ordered<Result>[]} results
 * @param {string[]} suggestions List of diagram keys to suggest to user for axes
 * @param {Benchmark} benchmark
 * @returns {React.ReactElement}
 * @constructor
 */
function LineChart({
    results,
    suggestions,
    benchmark,
}: {
    results: Ordered<Result>[];
    suggestions?: Suggestion[];
    benchmark?: Benchmark;
}): ReactElement {
    const [displayMode, setDisplayMode] = useState(Mode.Simple);

    const [xAxis, setXAxis] = useState('');
    const [yAxis, setYAxis] = useState('');

    // grouping-by-site behaviour
    // Linear and Logarithmic mode require numeric x / column values
    // splits results from different sites into different datasets
    // map site.id => object with array of data points
    type DataPoint = { x: number; y: number };
    const data = new Map<string, { siteName: string; data: DataPoint[] }>();
    const labelSet = new Set<number>();

    let rejectedResults: { result: Ordered<Result>; reason: string }[] = [];

    if (xAxis.length && yAxis.length) {
        for (const result of results) {
            const x = fetchSubkey(result.json, xAxis);
            const y = fetchSubkey(result.json, yAxis);

            if (typeof fetchSubkey(result.json, xAxis) !== 'number') {
                rejectedResults.push({ result, reason: 'X axis value not numeric' });
                continue;
            }
            if (typeof fetchSubkey(result.json, yAxis) !== 'number') {
                rejectedResults.push({ result, reason: 'Y axis value not numeric' });
                continue;
            }
            if (data.get(result.site.id) === undefined) {
                data.set(result.site.id, {
                    siteName: result.site.name,
                    data: [],
                });
            }
            data.get(result.site.id)?.data.push({ x: x as number, y: y as number });
            labelSet.add(x as number);
        }
    }

    // generate datasets
    const datasets: ChartDataset<'line'>[] = [];
    let colorIndex = 0;
    data.forEach(function (dataMeta, site, _) {
        datasets.push({
            label: dataMeta.siteName,
            backgroundColor: BACKGROUND_COLORS[colorIndex],
            borderColor: CHART_COLORS[colorIndex],
            borderWidth: 1,
            data: dataMeta.data.sort((a: DataPoint, b: DataPoint) => a.x - b.x),
            spanGaps: true,
        });
        colorIndex++;
    });

    const labels = Array.from(labelSet).sort((a, b) => a - b);

    return (
        <>
            <Form.Group className="mb-1">
                <Form.Label>Mode:</Form.Label>
                <Form.Select
                    onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                        setDisplayMode(parseInt(e.target.value));
                    }}
                >
                    <option value={Mode.Linear}>Linear</option>
                    <option value={Mode.Logarithmic}>Logarithmic</option>
                </Form.Select>
            </Form.Group>
            <Form.Group className="mb-1">
                <Form.Label>X Axis:</Form.Label>
                <InputWithSuggestions
                    placeholder="machine.cpu.count"
                    setInput={(i) => setXAxis(i)}
                    suggestions={suggestions}
                />
            </Form.Group>
            <Form.Group>
                <Form.Label>Y Axis:</Form.Label>
                <InputWithSuggestions
                    placeholder="result.score"
                    setInput={(i) => setYAxis(i)}
                    suggestions={suggestions}
                />
            </Form.Group>

            {rejectedResults.length > 0 && (
                <div className="my-1">
                    {datasets.length > 0 &&
                        rejectedResults.map((rejected) => (
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
                <Line
                    data={{ labels, datasets }}
                    options={{
                        animation: false,
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                            },
                            title: {
                                display: true,
                                text: 'Line Graph',
                            },
                            tooltip: {
                                callbacks: {
                                    title: function (tooltipItem: TooltipItem<'line'>[]) {
                                        return tooltipItem[0].label;
                                    },
                                },
                            },
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: xAxis,
                                },
                            },
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: yAxis,
                                },
                                type: displayMode === Mode.Logarithmic ? 'logarithmic' : 'linear',
                            },
                        },
                        elements: {
                            line: {
                                tension: 0,
                            },
                        },
                    }}
                />
            )}

            {/* TODO: download png / csv buttons */}
        </>
    );
}

const LineChartMeta = {
    element: LineChart,
    name: 'Line Chart',
    id: '0',
};

export default LineChartMeta;
