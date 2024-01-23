const categoryButtons = document.getElementsByClassName("category-btn");
const productCards = document.getElementsByClassName("product-card");
const sortButtons = document.getElementsByClassName("sort-btn");
const ratingStarsArray = document.getElementsByClassName("rating-star");

//loop over rating stars and adjust fill Color based on rating
for (let ratingStar of ratingStarsArray) {
  if (ratingStar.dataset.rating && ratingStar.dataset.avgRating) {
    handleRatingStarColor(
      ratingStar,
      parseFloat(ratingStar.dataset.rating),
      parseFloat(ratingStar.dataset.avgRating) / 100,
    );
  }
}

// handle category selection
for (let button of categoryButtons) {
  button.addEventListener("click", (e) => {
    if (e.target.dataset.category) {
      handleCategoryClick(e.target.dataset.category);
    }
  });
}

// handle product sorting
for (let button of sortButtons) {
  button.addEventListener("click", (e) => {
    console.log("sort button clicked");
    handleSortButtonClock(e.target.dataset.sorting);
  });
}

// filter product list of the shop by checking if a category button was clicked
function handleCategoryClick(category) {
  console.log(category);

  for (let product of productCards) {
    if (product.dataset.category === category) {
      product.classList.remove("hidden");
    } else {
      product.classList.add("hidden");
    }
  }
}

// send the selected sort criteria to the products view
function handleSortButtonClock(sorting) {
  let currentURL = new URL(window.location);
  let sort;
  let direction;

  // prepare sort parameters
  if (sorting === "price-low-to-high") {
    sort = "price";
    direction = "asc";
  } else if (sorting === "price-high-to-low") {
    sort = "price";
    direction = "desc";
  } else if (sorting === "name-a-to-z") {
    sort = "name";
    direction = "asc";
  } else if (sorting === "name-z-to-a") {
    sort = "name";
    direction = "desc";
  } else {
    return;
  }

  // add the sort parameters to url
  currentURL.searchParams.set("sort", sort);
  currentURL.searchParams.set("direction", direction);

  window.location.replace(currentURL);
}

// set fill color of a rating star element
function handleRatingStarColor(ratingStarEl, rating, averageRating) {
  console.log(rating, averageRating);
  if (rating <= averageRating) {
    ratingStarEl.style.color = "rgb(250,202,21)";
  } else {
    ratingStarEl.style.fill = "rgb(229 231 235";
  }
}
