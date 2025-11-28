
const userBtn = document.getElementById("userBtn");
const feedbackPopup = document.getElementById("feedbackPopup");
const closeFeedback = document.getElementById("closeFeedback");
const thankYouPopup = document.getElementById("thankYouPopup");
const closeThankYou = document.getElementById("closeThankYou");
const stars = document.querySelectorAll(".star");
let selectedRating = 0;

userBtn.addEventListener("click", () => {
  feedbackPopup.style.display = "block";
});


closeFeedback.addEventListener("click", () => {
  feedbackPopup.style.display = "none";
});

// Close if click outside feedback content
window.addEventListener("click", (e) => {
  if (e.target === feedbackPopup) feedbackPopup.style.display = "none";
  if (e.target === thankYouPopup) thankYouPopup.style.display = "none";
});


closeThankYou.addEventListener("click", () => {
  thankYouPopup.style.display = "none";
});

// Star rating logic
stars.forEach((star, idx) => {
  star.addEventListener("mouseover", () => {
    star.style.color = "gold";
  });

  star.addEventListener("mouseout", () => {
    star.style.color = selectedRating > idx ? "gold" : "gray";
  });

  star.addEventListener("click", () => {
    selectedRating = idx + 1;
    stars.forEach((s, i) => {
      s.classList.toggle("selected", i < selectedRating);
      s.style.color = i < selectedRating ? "gold" : "gray";
    });
  });
});

function showThankYou() {
  thankYouPopup.style.display = "block";
  setTimeout(() => {
    thankYouPopup.style.display = "none";
  }, 2000);
}

// Submit feedback
document
  .getElementById("feedbackForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const review = document.getElementById("review").value;

    if (selectedRating === 0) {
      alert("Please select a rating!");
      return;
    }

    try {
      const response = await fetch("/submit_feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, rating: selectedRating, review }),
      });
      const result = await response.json();

      if (result.success) {
        feedbackPopup.style.display = "none";
        document.getElementById("feedbackForm").reset();
        stars.forEach((s) => {
          s.classList.remove("selected");
          s.style.color = "gray";
        });
        selectedRating = 0;
        showThankYou(); 
      } else {
        alert("Error submitting feedback!");
      }
    } catch (err) {
      alert("Server error. Please try again later.");
    }
  });
