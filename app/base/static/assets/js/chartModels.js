function barChartJS(sourceName, labels, values) {
    const background = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ];
    const borderColor = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ];
    const borderWidth = 1;
    const options = {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    const data = {
        labels: labels,
        datasets: [{
            label: sourceName,
            data: values,
            background: background,
            borderColor: borderColor,
            borderWidth: borderWidth
        }]
    };
    
    const config = {
        type: "bar",
        data: data,
        options: options
    };

    return config;
};