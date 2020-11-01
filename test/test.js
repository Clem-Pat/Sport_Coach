
function stop(){
    alert('stop');
}

document.addEventListener('DOMContentLoaded', drawChart);

function drawChart(){

    var lLabels = [];
    for (var i = 0; i <= 50; i++) {
        lLabels.push(i);
    }

    var currentData=[];
    currentData.push({x: 5, y: 120});
    currentData.push({x: 20, y: 135});
    currentData.push({x: 25, y: 122});

    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: lLabels,
            datasets: [{
                label: 'My First dataset',
                borderColor: 'rgb(0, 0, 255)',
                fill: false,
                data: currentData,
                lineTension: 0
            },
            {
                label: 'My Second dataset',
                borderColor: '#ffa900',
                fill: false,
                data: [{x: 10, y: 120},
                       {x: 40, y: 135},
                       {x: 50, y: 122}],
                lineTension: 0
            }]
        },
        options: {animation: {duration: 0}}
    });
}
