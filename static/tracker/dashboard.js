// dashboard.js

document.addEventListener("DOMContentLoaded", function () {
  fetchChartData();
});

async function fetchChartData() {
  try {
    const response = await fetch("/api/chart-data/"); // Replace with your actual API endpoint
    const data = await response.json();
    renderChart(data);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  }
}

function renderChart(data) {
    console.log("data:",data);
  const ctx = document.getElementById("incomeExpensesChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.months,
      datasets: [
        {
          label: "Income",
          data: data.income_data,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
        {
          label: "Expenses",
          data: data.expenses_data,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
