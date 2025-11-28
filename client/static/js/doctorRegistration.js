const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor");
const doctorForm = document.getElementById("doctorForm");
const successPopup = document.getElementById("successPopup");
const closeSuccess = document.getElementById("closeSuccess");
const successMessage = document.getElementById("successMessage");

const licenseInput = document.getElementById("licenseInput");
const licenseStatus = document.getElementById("licenseStatus");

doctorBtn?.addEventListener("click", () => doctorPopup.classList.add("active"));

closeDoctor?.addEventListener("click", () =>
  doctorPopup.classList.remove("active")
);

// Helper function to capitalize first letter
function capitalizeFirstLetter(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Validate govt license email (ABC123@gov.ac.in)
function validateLicense(email) {
  const licenseRegex = /^[A-Z]{3}[0-9]{3}@gov\.ac\.in$/;
  return licenseRegex.test(email);
}

// Live validation of license with 2.5s spinner
licenseInput?.addEventListener("input", () => {
  const value = licenseInput.value.trim();

  licenseStatus.textContent = "";
  licenseStatus.style.color = "black";

  if (!value) return;

  // Show spinner while "verifying"
  licenseStatus.innerHTML = '<span class="spinner"></span> Verifying...';
  licenseStatus.style.color = "orange";

  setTimeout(() => {
    if (validateLicense(value)) {
      licenseStatus.textContent = "✔ Verified";
      licenseStatus.style.color = "green";
    } else {
      licenseStatus.textContent = "✖ Invalid";
      licenseStatus.style.color = "red";
    }
  }, 2500);
});

// Form submission
doctorForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(doctorForm);

  // Capitalize location
  if (formData.has("location")) {
    const locationValue = formData.get("location");
    formData.set("location", capitalizeFirstLetter(locationValue));
  }

  if (!validateLicense(formData.get("license"))) {
    alert("⚠️ Invalid Govt License Email. Please check.");
    return;
  }

  const experience = formData.get("experience");
  const phone = formData.get("phone");
  if (isNaN(experience) || experience < 0) {
    alert("⚠️ Please enter a valid number for Experience.");
    return;
  }

  if (!/^\+?\d{10,15}$/.test(phone)) {
    alert("⚠️ Please enter a valid phone number.");
    return;
  }

  try {
    const response = await fetch("/register_doctor", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();

    if (result.success) {
      doctorForm.reset();
      licenseStatus.textContent = "";
      successMessage.innerHTML =
        "✅ Successfully Registered! Visit Support page if needed.";
      successPopup.classList.add("show");
      setTimeout(() => successPopup.classList.remove("show"), 5000);
      setTimeout(() => doctorPopup.classList.remove("active"), 500);
    } else {
      alert(result.message || "⚠️ Registration failed.");
    }
  } catch (err) {
    console.error(err);
    alert("⚠️ Server error. Please contact support.");
  }
});


closeSuccess?.addEventListener("click", () =>
  successPopup.classList.remove("show")
);
