// static/js/dashboard.js
// Dashboard charts and statistics
function initializeDashboardCharts() {
    // Request Status Chart
    const statusCtx = document.getElementById('requestStatusChart');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'In Progress', 'Resolved', 'Closed'],
                datasets: [{
                    data: [
                        parseInt(statusCtx.dataset.pending || 0),
                        parseInt(statusCtx.dataset.inProgress || 0),
                        parseInt(statusCtx.dataset.resolved || 0),
                        parseInt(statusCtx.dataset.closed || 0)
                    ],
                    backgroundColor: [
                        '#ffc107',
                        '#17a2b8',
                        '#0f9d58',
                        '#5f6368'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Monthly Trends Chart
    const trendsCtx = document.getElementById('monthlyTrendsChart');
    if (trendsCtx) {
        fetch('/dashboard/api/monthly-stats/')
            .then(response => response.json())
            .then(data => {
                new Chart(trendsCtx, {
                    type: 'line',
                    data: {
                        labels: data.map(item => item.month),
                        datasets: [{
                            label: 'Service Requests',
                            data: data.map(item => item.count),
                            borderColor: '#1a73e8',
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
    }
}