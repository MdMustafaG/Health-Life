document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Dashboard Data (Doctors & Specializations)
    const res = await fetch("/dashboard/data");
    const result = await res.json();

    if (!result.success) return console.error(result.message);

    const data = result.data;

    // Total Doctors
    document.getElementById("totalDoctors").textContent = data.total_doctors || 0;

    // Specialization Chart
    const specCanvas = document.getElementById("specializationChart");
    if (specCanvas) {
      new Chart(specCanvas.getContext("2d"), {
        type: "doughnut",
        data: {
          labels: data.specializations.map((s) => s.specialization),
          datasets: [
            {
              data: data.specializations.map((s) => s.count),
              backgroundColor: ["#1da1f2", "#00ffcc", "#ff6384", "#ff9f40", "#36a2eb", "#9966ff"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { position: "bottom" } },
        }
      });
    }

    // Feedback Ratings Chart
    const feedbackRes = await fetch("/dashboard/feedback_ratings");
    const feedbackResult = await feedbackRes.json();

    if (!feedbackResult.success) return console.error(feedbackResult.message);

    const feedbackCanvas = document.getElementById("feedbackChart");

    if (feedbackCanvas) {
      const ratings = ["1", "2", "3", "4", "5"];
      const ratingCounts = ratings.map(r => feedbackResult.data.feedback_ratings[r] || 0);

      const totalRatings = ratingCounts.reduce((a, b) => a + b, 0);

      // Update "Total Ratings" text ONLY once
      const totalText = document.getElementById("totalRatingsText");
      if (totalText) totalText.textContent = `Total Ratings: ${totalRatings}`;

      new Chart(feedbackCanvas.getContext("2d"), {
        type: "bar",
        data: {
          labels: ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
          datasets: [{
            label: "Users",
            data: ratingCounts,
            backgroundColor: [
              "rgba(255,77,79,0.9)",
              "rgba(255,136,56,0.9)",
              "rgba(255,219,50,0.9)",
              "rgba(110,207,57,0.9)",
              "rgba(54,207,201,0.95)"
            ],
            borderColor: "rgba(255,255,255,0.3)",
            borderWidth: 2,
            barPercentage: 0.45,
            categoryPercentage: 0.55
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            title: { display: false }  //  NO duplicate TOTAL RATINGS
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                display: false,      //  Hide 0,1,2,3 numbers
              },
              grid: { display: false }
            },
            x: {
              ticks: { color: "#b1c7ff" },
              grid: { display: false }
            }
          }
        }
      });
    }

  } catch (err) {
    console.error("Dashboard JS Error:", err);
  }
});
