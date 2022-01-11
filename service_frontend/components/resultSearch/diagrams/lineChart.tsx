import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Benchmark, Result } from 'model';
import { Form } from 'react-bootstrap';
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
    LogarithmicScale,
    LineElement,
    PointElement,
    ScatterDataPoint,
    Title,
    Tooltip,
    TooltipItem
} from 'chart.js';
import { Suggestion } from '../jsonSchema';

ChartJS.register(CategoryScale, LinearScale, LogarithmicScale, LineElement, Title, Tooltip, Legend, PointElement);

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
    'rgb(201, 203, 207)' // gray
];

const BACKGROUND_COLORS = [
    'rgba(255, 99, 132, 0.5)', // red
    'rgba(255, 159, 64, 0.5)', // orange
    'rgba(255, 205, 86, 0.5)', // yellow
    'rgba(75, 192, 192, 0.5)', // green
    'rgba(54, 162, 235, 0.5)', // blue
    'rgba(153, 102, 255, 0.5)', // purple
    'rgba(201, 203, 207, 0.5)' // gray
];

/**
 * Chart displaying a line diagram following the results' ordering
 * @param {Ordered<Result>[]} results
 * @param {string[]} suggestions List of diagram keys to suggest to user for axes
 * @param {Benchmark} benchmark
 * @returns {React.ReactElement}
 * @constructor
 */
function LineChart(
    {
        results,
        suggestions,
        benchmark
    }: { results: Ordered<Result>[]; suggestions?: Suggestion[]; benchmark?: Benchmark }
): ReactElement {
    const [displayMode, setDisplayMode] = useState(Mode.Simple);

    const [groupBySite, setGroupBySite] = useState(false);

    const [xAxis, setXAxis] = useState('');
    const [yAxis, setYAxis] = useState('');

    function analyzeData(results: Ordered<Result>[]) {
        let sameSite = true;
        let columnsAreNumbers = true;

        // test if sites are the same all across and if it's an integer range
        if (results.length !== 0) {
            const siteId = results[0].site.id;
            for (const result of results) {
                sameSite = sameSite && result.site.id === siteId;
                columnsAreNumbers =
                    columnsAreNumbers &&
                    typeof fetchSubkey(result.json, xAxis) === 'number';
            }
        } else {
            sameSite = false;
            columnsAreNumbers = false;
        }

        return {
            sameSite,
            columnsAreNumbers
        };
    }

    const properties = analyzeData(results);

    function processInput(results: Ordered<Result>[]): ChartData<'line', (number | ScatterDataPoint | null)[]> {
        const labels = []; // labels below graph

        // grouping-by-site behaviour
        // Linear and Logarithmic mode require numeric x / column values
        // splits results from different sites into different datasets
        if (groupBySite && (displayMode === Mode.Linear || displayMode === Mode.Logarithmic)) {
            // map site.id => object with array of data points
            const datasets = new Map<string,
                { siteName: string; data: { x: number; y: number }[] }>();
            const labelSet = new Set<number>();

            for (const result of results) {
                const x = fetchSubkey(result.json, xAxis) as number;
                const y = fetchSubkey(result.json, yAxis) as number;
                if (datasets.get(result.site.id) === undefined) {
                    datasets.set(result.site.id, {
                        siteName: result.site.name,
                        data: []
                    });
                }
                datasets.get(result.site.id)?.data.push({ x, y });
                labelSet.add(x);
            }

            // generate datasets
            const data: ChartDataset<'line'>[] = [];
            let colorIndex = 0;
            datasets.forEach(function(dataMeta, site, _) {
                data.push({
                    label: dataMeta.siteName,
                    backgroundColor: BACKGROUND_COLORS[colorIndex],
                    borderColor: CHART_COLORS[colorIndex],
                    borderWidth: 1,
                    data: dataMeta.data,
                    spanGaps: true
                });
                colorIndex++;
            });

            return {
                labels: Array.from(labelSet).sort((a, b) => a - b),
                datasets: data
            };
        }

        const dataPoints = [];

        // display all results as a single dataset
        for (const result of results) {
            const x = fetchSubkey(result.json, xAxis) as number;
            const y = fetchSubkey(result.json, yAxis) as number;
            if (x === undefined || y === undefined) {
                continue;
            }
            let label = x.toString();
            if (!properties.sameSite) {
                label += ' (' + result.site.name + ')';
            }
            dataPoints.push({ x, y });
            labels.push(label);
        }

        return {
            labels: labels,
            datasets: [
                {
                    label: getSubkeyName(yAxis),
                    backgroundColor: BACKGROUND_COLORS[0],
                    borderColor: CHART_COLORS[0],
                    borderWidth: 1,
                    data: dataPoints,
                    spanGaps: true
                }
            ]
        };
    }

    return (
        <>
            <Form.Group className='mb-1'>
                <Form.Select
                    onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                        setDisplayMode(parseInt(e.target.value));
                    }}
                >
                    <option value={Mode.Simple}>Simple</option>
                    <option value={Mode.Linear} disabled={!properties.columnsAreNumbers}>
                        Linear
                    </option>
                    <option
                        value={Mode.Logarithmic}
                        disabled={!properties.columnsAreNumbers}
                    >
                        Logarithmic
                    </option>
                </Form.Select>
            </Form.Group>
            <Form.Group className='mb-1'>
                <Form.Check
                    type='switch'
                    label='Group values by site (only in linear & logarithmic mode)'
                    onChange={(e) => setGroupBySite(e.target.checked)}
                    disabled={displayMode !== Mode.Linear && displayMode !== Mode.Logarithmic}
                />
            </Form.Group>
            <Form.Group className='mb-1'>
                <InputWithSuggestions
                    placeholder='X axis'
                    setInput={(i) => setXAxis(i)}
                    suggestions={suggestions}
                />
            </Form.Group>
            <Form.Group>
                <InputWithSuggestions
                    placeholder='Y axis'
                    setInput={(i) => setYAxis(i)}
                    suggestions={suggestions}
                />
            </Form.Group>

            {xAxis.length > 0 && yAxis.length > 0 && (
                <Line
                    data={processInput(results)}
                    options={{
                        animation: false,
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            },
                            title: {
                                display: true,
                                text: 'Line Graph'
                            },
                            tooltip: {
                                callbacks: {
                                    title: function(tooltipItem: TooltipItem<'line'>[]) {
                                        return tooltipItem[0].label;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: xAxis
                                }
                            },
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: yAxis
                                },
                                type: displayMode === Mode.Logarithmic ? 'logarithmic' : 'linear'
                            }
                        },
                        elements: {
                            line: {
                                tension: 0
                            }
                        }
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
    id: '0'
};

export default LineChartMeta;
