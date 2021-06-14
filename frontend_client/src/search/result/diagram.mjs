import { search_page } from './searchPage.mjs';
import {
    clear_select,
    fetch_subkey,
    get_subkey_name,
    JSON_KEYS,
    validate_keypath,
} from './helpers.mjs';
import { JSONValueInputPrompt } from './jsonValueInputPrompt.mjs';
import { Table } from './resultTable.mjs';

const CHART_COLORS = [
    'rgb(255, 99, 132)', // red
    'rgb(255, 159, 64)', // orange
    'rgb(255, 205, 86)', // yellow
    'rgb(75, 192, 192)', // green
    'rgb(54, 162, 235)', // blue
    'rgb(153, 102, 255)', // purple
    'rgb(201, 203, 207)', // gray
];

export class Diagram {
    /**
     * Set the list of notable keys.
     *
     * These may be used as suggested fields to the user when selecting data sources.
     *
     * @param notable_keys
     */
    update_notable_keys(notable_keys) {}

    /**
     * Take in new data.
     * @param results an array of results to display
     */
    updateData(results) {}

    /**
     * Clean-up function/destructor.
     *
     * Called when using is swapping to another diagram.
     */
    cleanup() {}

    /**
     * Generic callback for when the user changes any setting, if you want to do it nice and polymorphic.
     */
    update_diagram_configuration() {}
}

export class SpeedupDiagram extends Diagram {
    /**
     * Build a new speedup diagram.
     */
    constructor() {
        super();
        this.results = [];
        this.xAxis = '';
        this.yAxis = '';
        this.notable_keys = [];
        this.mode = 'simple';
        this.grouping = false;

        document.getElementById('diagramConfiguration-speedup').classList.remove('d-none');

        let section = document.getElementById('diagramSection');
        {
            let xAxisDiv = document.createElement('div');
            xAxisDiv.classList.add('form-inline');
            {
                let label = document.createElement('label');
                label.for = 'diagramX';
                label.textContent = 'X Axis:';
                label.style.paddingRight = '0.2em';
                xAxisDiv.appendChild(label);

                let inputGroup = document.createElement('div');
                inputGroup.classList.add('input-group');

                this.xAxisInput = document.createElement('input');
                this.xAxisInput.type = 'text';
                this.xAxisInput.placeholder = 'path.to.value';
                this.xAxisInput.classList.add('form-control');
                this.xAxisInput.onchange = function () {
                    search_page.get_diagram()._update();
                };
                inputGroup.appendChild(this.xAxisInput);

                let inputGroupAppend = document.createElement('div');
                inputGroupAppend.classList.add('input-group-append');

                let xAxisDropdownButton = document.createElement('button');
                xAxisDropdownButton.classList.add(
                    'btn',
                    'btn-outline-secondary',
                    'dropdown-toggle',
                    'dropdown-toggle-split'
                );
                inputGroupAppend.appendChild(xAxisDropdownButton);
                this.xAxisJsonSelector = new JSONValueInputPrompt(
                    xAxisDropdownButton,
                    this.xAxisInput
                );

                inputGroup.appendChild(inputGroupAppend);
                xAxisDiv.appendChild(inputGroup);
            }
            section.appendChild(xAxisDiv);

            let yAxisDiv = document.createElement('div');
            yAxisDiv.classList.add('form-inline');
            {
                let label = document.createElement('label');
                label.for = 'diagramY';
                label.textContent = 'Y Axis:';
                label.style.paddingRight = '0.2em';
                yAxisDiv.appendChild(label);

                let inputGroup = document.createElement('div');
                inputGroup.classList.add('input-group');

                this.yAxisInput = document.createElement('input');
                this.yAxisInput.type = 'text';
                this.yAxisInput.placeholder = 'path.to.value';
                this.yAxisInput.classList.add('form-control');
                this.yAxisInput.onchange = function () {
                    search_page.get_diagram()._update();
                };
                inputGroup.appendChild(this.yAxisInput);

                let inputGroupAppend = document.createElement('div');
                inputGroupAppend.classList.add('input-group-append');

                let yAxisDropdownButton = document.createElement('button');
                yAxisDropdownButton.classList.add(
                    'btn',
                    'btn-outline-secondary',
                    'dropdown-toggle',
                    'dropdown-toggle-split'
                );
                inputGroupAppend.appendChild(yAxisDropdownButton);
                this.yAxisJsonSelector = new JSONValueInputPrompt(
                    yAxisDropdownButton,
                    this.yAxisInput
                );

                inputGroup.appendChild(inputGroupAppend);
                yAxisDiv.appendChild(inputGroup);
            }
            section.appendChild(yAxisDiv);

            let canvas = document.createElement('canvas');
            canvas.id = 'speedup';
            section.appendChild(canvas);

            let interactions = document.createElement('div');
            {
                let downloadButton = document.createElement('button');
                downloadButton.id = 'downloadButton';
                downloadButton.type = 'button';
                downloadButton.classList.add('btn', 'btn-light');
                downloadButton.textContent = 'Download as PNG';
                downloadButton.onclick = function () {
                    search_page.get_diagram().downloadPNG();
                };
                interactions.appendChild(downloadButton);

                let csvButton = document.createElement('button');
                csvButton.id = 'csvButton';
                csvButton.type = 'button';
                csvButton.classList.add('btn', 'btn-light');
                csvButton.textContent = 'Download as CSV';
                csvButton.onclick = function () {
                    search_page.get_diagram().downloadCSV();
                };
                interactions.appendChild(csvButton);
            }
            section.appendChild(interactions);
        }
    }

    /**
     * Pass various checks over the used data to verify if certain diagram modes are viable.
     *
     * sameSite: all results are from the same site
     * columnsAreNumbers: all columns/labels are actual numbers and can for example be put on a log scale
     *
     * @returns {{sameSite: boolean, columnsAreNumbers: boolean}}
     * @private
     */
    _determineDataProperties() {
        let sameSite = true;
        let columnsAreNumbers = true;

        // test if sites are the same all across and if it's an integer range
        if (this.results.length !== 0) {
            const site_path = JSON_KEYS.get(Table.DEFAULT_COLUMNS.SITE);
            let siteName = fetch_subkey(this.results[0], site_path);
            for (const result of this.results) {
                sameSite &&= fetch_subkey(result, site_path) === siteName;
                columnsAreNumbers &&= typeof fetch_subkey(result.data, this.xAxis) === 'number';
            }
        } else {
            sameSite = false;
            columnsAreNumbers = false;
        }

        return {
            sameSite,
            columnsAreNumbers,
        };
    }

    /**
     * Build a chart.js dataset off current data
     *
     * TODO: add nulls for columns this dataset has no value for
     *
     * @returns {{data: [{spanGaps: boolean, backgroundColor: *, borderColor: string|string, data: [], borderWidth: number, label: *|string}], labels: []}}
     * @private
     */
    _generateChartData(properties) {
        let labels = []; // labels below graph
        let dataPoints = [];
        let color = Chart.helpers.color;

        // grouping-by-site behaviour
        if (this.grouping === true && (this.mode === 'linear' || this.mode === 'log')) {
            let datasets = new Map();
            let labelSet = new Set();

            for (const result of this.results) {
                const x = fetch_subkey(result.data, this.xAxis);
                const y = fetch_subkey(result.data, this.yAxis);
                let label = x.toString();
                if (datasets.get(result.site) === undefined) {
                    datasets.set(result.site, []);
                }
                datasets.get(result.site).push({ x, y });
                dataPoints.push({ x, y });
                labelSet.add(label);
            }

            let data = [];
            let colorIndex = 0;
            datasets.forEach(function (dataset, site, _) {
                data.push({
                    label: site,
                    backgroundColor: color(CHART_COLORS[colorIndex]).alpha(0.5).rgbString(),
                    borderColor: CHART_COLORS[colorIndex],
                    borderWidth: 1,
                    data: dataset,
                    spanGaps: true,
                });
                colorIndex++;
            });

            return {
                labels: Array.from(labelSet).sort(),
                data: data,
            };
        }

        // default behaviour
        for (const result of this.results) {
            const x = fetch_subkey(result.data, this.xAxis);
            const y = fetch_subkey(result.data, this.yAxis);
            let label = x.toString();
            if (!properties.sameSite) {
                label +=
                    ' (' + fetch_subkey(result, JSON_KEYS.get(Table.DEFAULT_COLUMNS.SITE)) + ')';
            }
            dataPoints.push({ x, y });
            labels.push(label);
        }

        return {
            labels: labels,
            data: [
                {
                    label: get_subkey_name(this.yAxis),
                    backgroundColor: color(CHART_COLORS[0]).alpha(0.5).rgbString(),
                    borderColor: CHART_COLORS[0],
                    borderWidth: 1,
                    data: dataPoints,
                    spanGaps: true,
                },
            ],
        };
    }

    /**
     * Generate & download currently displayed data as a csv file.
     */
    downloadCSV() {
        let download = document.createElement('a');
        let dataHeader = 'data:text/csv;charset=utf-8,';
        let rows = [this.xAxis + ',' + this.yAxis + ',site'];
        for (const row of this.results) {
            let x = fetch_subkey(row.data, this.xAxis);
            let y = fetch_subkey(row.data, this.yAxis);
            let site = fetch_subkey(row, JSON_KEYS.get(Table.DEFAULT_COLUMNS.SITE));
            rows.push(x.toString() + ',' + y.toString() + ',' + site.toString());
        }
        download.href = encodeURI(dataHeader + rows.join('\r\n'));
        download.download = 'data.csv';
        download.click();
    }

    /**
     * Download a picture copy of the current diagram.
     */
    downloadPNG() {
        let download = document.createElement('a');
        let context = document.getElementById('speedup');
        download.href = context.toDataURL('image/png');
        download.download = 'diagram.png';
        download.click();
    }

    /**
     * Update the array of notable keys.
     * @param notable_keys The notable keys to make selectable for axis.
     */
    update_notable_keys(notable_keys) {
        this.notable_keys = notable_keys;

        // pick something by default
        this.xAxisInput.value = notable_keys[0];
        this.yAxisInput.value = notable_keys[0];
    }

    /**
     * Update diagram chart
     */
    refresh() {
        let { labels: labels, data: dataSets } = this._generateChartData(this.properties);

        if (window.diagram !== undefined && window.diagram !== null) {
            window.diagram.data.labels = labels;
            window.diagram.data.datasets = dataSets;

            window.diagram.options.scales.yAxes[0].scaleLabel.labelString = this.yAxis;
            window.diagram.options.scales.xAxes[0].scaleLabel.labelString = this.xAxis;

            if (this.mode === 'log') {
                window.diagram.options.scales.xAxes[0].type = 'logarithmic';
                window.diagram.options.scales.yAxes[0].type = 'logarithmic';
            } else if (this.mode === 'linear') {
                window.diagram.options.scales.xAxes[0].type = 'linear';
                window.diagram.options.scales.yAxes[0].type = 'linear';
            } /* simple */ else {
                delete window.diagram.options.scales.xAxes[0].type;
                window.diagram.options.scales.yAxes[0].type = 'linear';
            }

            window.diagram.update();
        } else {
            let context = document.getElementById('speedup').getContext('2d');
            let configuration = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: dataSets,
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Line Graph',
                    },
                    scales: {
                        yAxes: [
                            {
                                ticks: {
                                    beginAtZero: true,
                                },
                                scaleLabel: {
                                    display: true,
                                    labelString: this.yAxis,
                                },
                            },
                        ],
                        xAxes: [
                            {
                                scaleLabel: {
                                    display: true,
                                    labelString: this.xAxis,
                                },
                            },
                        ],
                    },
                    elements: {
                        line: {
                            tension: 0,
                        },
                    },
                    tooltips: {
                        callbacks: {
                            title: function (tooltipItem, _) {
                                return tooltipItem[0].yLabel + ' (' + tooltipItem[0].label + ')';
                            },
                        },
                    },
                },
            };
            if (this.mode === 'log') {
                configuration.options.scales.xAxes[0].type = 'logarithmic';
                configuration.options.scales.yAxes[0].type = 'logarithmic';
            } else if (this.mode === 'linear') {
                configuration.options.scales.xAxes[0].type = 'linear';
                configuration.options.scales.yAxes[0].type = 'linear';
            } /* simple */ else {
                delete configuration.options.scales.xAxes[0].type;
                configuration.options.scales.yAxes[0].type = 'linear';
            }
            window.diagram = new Chart(context, configuration);
        }

        document.getElementById('downloadButton').disabled = false;
        document.getElementById('csvButton').disabled = false;
    }

    _update() {
        this.xAxis = this.xAxisInput.value;
        this.yAxis = this.yAxisInput.value;

        this.properties = this._determineDataProperties();

        document
            .getElementById('speedupDiagramMode')
            .children.namedItem('speedupDiagramMode-linear').disabled =
            !this.properties.columnsAreNumbers;
        document
            .getElementById('speedupDiagramMode')
            .children.namedItem('speedupDiagramMode-log').disabled =
            !this.properties.columnsAreNumbers;

        if (
            this.properties.columnsAreNumbers === false &&
            (this.mode === 'log' || this.mode === 'linear')
        ) {
            this.mode = 'simple';
            document.getElementById('speedupDiagramMode').value = 'simple';
        }

        if (
            !validate_keypath(this.xAxis) ||
            !validate_keypath(this.yAxis) ||
            this.results.length === 0
        ) {
            document.getElementById('downloadButton').disabled = 'true';
            document.getElementById('csvButton').disabled = 'true';
            document.getElementById('speedup').style.display = 'none';
            return;
        } else {
            document.getElementById('speedup').style.removeProperty('display');
        }

        this.refresh();
    }

    /**
     * Update diagram data
     * @param data The new results to use.
     */
    updateData(data) {
        this.results = data;

        this._update();
    }

    /**
     * Remove data associated to this component, such as chart.js objects and HTML elements.
     */
    cleanup() {
        if (window.diagram) {
            window.diagram.destroy();
            delete window.diagram;
        }

        document.getElementById('diagramConfiguration-speedup').classList.add('d-none');

        // naïve purge
        clear_select(document.getElementById('diagramSection'));
    }

    update_diagram_configuration() {
        this.mode = document.getElementById('speedupDiagramMode').value;
        this.grouping = document.getElementById('speedupDiagramGroupedMode').checked;
        this._update();
    }
}
