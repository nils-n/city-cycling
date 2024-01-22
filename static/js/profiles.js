// handle css of country field selector
let countrySelectorEl = document.querySelector(
  "select[name='default_country']",
);
const rateProductBtnArray = document.getElementsByClassName("rate-product-btn");
// Event Listeners for Rating
for (let rateBtn of rateProductBtnArray) {
  rateBtn.addEventListener("click", (e) => {
    console.log(e);
    console.log(e.target.dataset.productId);
    console.log(e.target.dataset.userId);
    console.log(e.target.dataset.rating);
    if (
      e.target.dataset.productId &&
      e.target.dataset.userId &&
      e.target.dataset.rating
    ) {
      handleRatingClick(
        e.target.dataset.productId,
        e.target.dataset.userId,
        e.target.dataset.rating,
      );
    }
  });
}

// set Country field to light gray by default
document.addEventListener("DOMContentLoaded", (event) => {
  setDefaultCountryFieldColor();
});

// set Country field to light gray when deselecting or selecting a country
countrySelectorEl.addEventListener("change", () => {
  updateCountryFieldColor();
});

// handle action when user clicks on a rating star
function handleRatingClick(productId, userId, rating) {
  console.log("productId, userId, rating", productId, userId, rating);
}

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
