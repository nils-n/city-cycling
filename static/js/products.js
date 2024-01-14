const categoryButtons = document.getElementsByClassName("category-btn");
const productCards = document.getElementsByClassName("product-card");
const sortButtons = document.getElementsByClassName("sort-btn");

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
    sort = "price";
    direction = "desc";
  } else {
    return;
  }

  // add the sort parameters to url
  currentURL.searchParams.set("sort", sort);
  currentURL.searchParams.set("direction", direction);

  window.location.replace(currentURL);
}
