/*
    The Diagram class is responsible of taking previously stored results and
    rendering them into a comparison diagram.
*/

let chartColors = [
    'rgb(255, 99, 132)', // red
    'rgb(255, 159, 64)', // orange
    'rgb(255, 205, 86)', // yellow
    'rgb(75, 192, 192)', // green
    'rgb(54, 162, 235)', // blue
    'rgb(153, 102, 255)', // purple
    'rgb(201, 203, 207)' // gray
];

class Diagram extends Content {
    // todo: add nulls for columns this dataset has no value for
    buildDataset(data, index) {
        let color = Chart.helpers.color;
        let scores = [];
        for (const value of data) {
            scores.push(value.score);
        }
        let dataSet = {
            label: 'score',
            backgroundColor: color(chartColors[index]).alpha(0.5).rgbString(),
            borderColor: chartColors[index],
            borderWidth: 1,
            data: scores,
            spanGaps: true
        };
        return dataSet;
    }

    // todo: sum of all datasets' core_counts
    buildLabels(data, index) {
        let labels = [];
        let sameSite = true;
        let siteName = data[0].site;
        for (const keypoint of data) {
            sameSite &&= (keypoint.site == siteName);
        }
        for (const value of data) {
            if (sameSite) {
                labels.push(value.core_count.toString());
            }
            else {
                labels.push(value.site + ', ' + value.core_count.toString());
            }
        }
        return labels;
    }

    generateCSV(dataIndex) {
        let dataHeader = "data:text/csv;charset=utf-8,";
        let rows = ["core_count,score"];
        for (const row of this.results[dataIndex]) {
            rows.push(row.core_count.toString() + "," + row.score.toString());
        }
        return dataHeader + rows.join("\r\n");
    }

    // update method inherited from Content
    update() {
        this.results = getData();

        let dataSets = [];
        for (let i = 0; i < this.results.length; i++) {
            let dataset = this.buildDataset(this.results[i], i);
            dataSets.push(dataset);
        }
        let labels = this.buildLabels(this.results[0]);

        let context = document.getElementById('speedup').getContext('2d');
        window.diagram = new Chart(context, {
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
                    text: 'Benchmark speedup'
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'score'
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'num_gpus'
                        }
                    }]
                }
            }
        });
    }
}

window.onload = function () {
    var diagram = new Diagram();

    let canvas = document.getElementById('speedup');
    let downloadButton = document.getElementById('download-button')
    downloadButton.addEventListener('click', function (e) {
        let dataURL = canvas.toDataURL('image/png');
        downloadButton.href = dataURL;
    });

    diagram.update();

    let csvButton = document.getElementById('csv-button');
    csvButton.addEventListener('click', function (e) {
        // TODO: defaults to dataset 0, selection not implemented due to
        // multiple-dataset functionality being absent
        let dataURI = encodeURI(diagram.generateCSV(0));
        csvButton.href = dataURI;
    });

};
