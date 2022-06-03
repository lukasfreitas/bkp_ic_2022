
function changeStatus(status){
    if(status){
        document.getElementById("live_status").className = "badge bg-success"; 
    }else{
        document.getElementById("live_status").className = "badge bg-danger"; 
    } 
};

function createChart(ctx, tittle,labels, values, color){
    const data = {
        labels: labels,
        datasets: [{
            label: tittle,
            data: values,
            fill: false,
            borderColor: color,
            tension: 0.1
        }]
    };
    const cfg = {
        type: 'line',
        data: data,
    };
    const chart_obj = new Chart(ctx, cfg);

    return chart_obj
}

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}