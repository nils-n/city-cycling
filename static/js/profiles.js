// handle css of country field selector
let countrySelectorEl = document.querySelector(
  "select[name='default_country']",
);

// set Country field to light gray by default
document.addEventListener("DOMContentLoaded", (event) => {
  setDefaultCountryFieldColor();
});

// set Country field to light gray when deselecting or selecting a country
countrySelectorEl.addEventListener("change", () => {
  updateCountryFieldColor();
});

function setDefaultCountryFieldColor() {
  countrySelectorEl.style.color = "#6b7280";
}

function updateCountryFieldColor() {
  if (countrySelectorEl.value === "") {
    countrySelectorEl.style.color = "#6b7280";
  } else {
    countrySelectorEl.style.color = "rgb(55,65,81)";
  }
}
