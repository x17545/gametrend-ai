let playerTrendChart = null;

async function loadPlayerTrendChart() {
  try {
    const data = await apiRequest("/api/data");

    const recentData = data
      .slice()
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .slice(-30);

    const labels = recentData.map((item) => item.date);
    const values = recentData.map((item) => item.value);

    const canvas = document.getElementById("playerTrendChart");

    if (!canvas) return;

    if (playerTrendChart) {
      playerTrendChart.destroy();
    }

    playerTrendChart = new Chart(canvas, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Daily Players",
            data: values,
            tension: 0.25,
            borderWidth: 2,
            pointRadius: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
          },
        },
        scales: {
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 45,
            },
          },
          y: {
            beginAtZero: false,
          },
        },
      },
    });
  } catch (error) {
    console.error("플레이어 추세 그래프 로딩 실패:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadPlayerTrendChart();
});