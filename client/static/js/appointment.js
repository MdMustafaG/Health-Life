function toggleDetails(button) {
  const card = button.closest(".doctor-card");
  if (!card) return;
  const details = card.querySelector(".doctor-details");
  if (!details) return;
  const modalDetails = document.getElementById("modal-details");
  modalDetails.innerHTML = details.innerHTML;
  const modal = document.getElementById("doctorModal");
  modal.style.display = "block";
}

function closeModal() {
  const modal = document.getElementById("doctorModal");
  modal.style.display = "none";
}

// Close modal when clicking outside modal content
window.onclick = function(event) {
  const modal = document.getElementById("doctorModal");
  if (event.target === modal) {
    modal.style.display = "none";
  }
}

// Filter doctors by city from dropdown
function filterByCity() {
  const city = document.getElementById("cityDropdown").value;
  if (city) {
    window.location.href = "/appointment?city=" + encodeURIComponent(city);
  } else {
    window.location.href = "/appointment";
  }
}
