fetch('/sales-data')
.then(res => res.json())
.then(result => {
    const labels = result.data.map(d => d[0]);
    const values = result.data.map(d => d[1]);

    new Chart(document.getElementById('chart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Sales',
                data: values
            }]
        }
    });
});
