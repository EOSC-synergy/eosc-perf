/*
    The Diagram class is responsible of taking previously stored results and
    rendering them into a comparison diagram.
*/

function getData() {
    return [
        [
            { corecount: 1, score: 1.0 },
            { corecount: 2, score: 1.33 },
            { corecount: 3, score: 1.5 },
            { corecount: 4, score: 1.6 },
            { corecount: 5, score: 1.66 },
            { corecount: 6, score: 1.71 },
            { corecount: 7, score: 1.75 },
            { corecount: 8, score: 1.77 },
            { corecount: 9, score: 1.79 },
            { corecount: 10, score: 1.81 },
            { corecount: 11, score: 1.83 },
            { corecount: 12, score: 1.84 },
            { corecount: 13, score: 1.85 },
            { corecount: 14, score: 1.86 },
            { corecount: 15, score: 1.875 }
        ]
    ];
}


let chartColors = [
    'rgb(255, 99, 132)', // red
    'rgb(255, 159, 64)', // orange
    'rgb(255, 205, 86)', // yellow
    'rgb(75, 192, 192)', // green
    'rgb(54, 162, 235)', // blue
    'rgb(153, 102, 255)', // purple
    'rgb(201, 203, 207)' // gray
];

function buildDataset(data, index) {
    let color = Chart.helpers.color;
    let scores = [];
    for (const value of data) {
        scores.push(value.score);
    }
    let dataSet = {
        label: 'dataset ' + index,
        backgroundColor: color(chartColors[index]).alpha(0.5).rgbString(),
        borderColor: chartColors[index],
        borderWidth: 1,
        data: scores
    };
    return dataSet;
}

class Diagram extends Content {
    // update method inherited from Content
    update() {
        let results = getData();

        let labels = [];
        let dataSets = [];
        for (let i = 0; i < results.length; i++) {
            labels.push('dataset ' + i.toString());
            let dataset = buildDataset(results[i], i);
            dataSets.push(dataset);
        }

        let context = document.getElementById('speedup').getContext('2d');
        window.diagram = new Chart(context, {
            type: 'bar',
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
                }
            }
        });
    }
}

diagram = new Diagram();

window.onload = function () {
    diagram.update();
};
