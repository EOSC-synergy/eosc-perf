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
        for (const value of data) {
            labels.push(value.core_count.toString() + ' cores');
        }
        return labels;
    }

    // update method inherited from Content
    update() {
        let results = getData();

        let dataSets = [];
        for (let i = 0; i < results.length; i++) {
            let dataset = this.buildDataset(results[i], i);
            dataSets.push(dataset);
        }
        let labels = this.buildLabels(results[0]);

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
                        }
                    }]
                }
            }
        });
    }
}

diagram = new Diagram();

window.onload = function () {
    var canvas = document.getElementById('speedup');
    let button = document.getElementById('download-button')
    button.addEventListener('click', function (e) {
        var dataURL = canvas.toDataURL('image/png');
        button.href = dataURL;
    });

    diagram.update();
};
