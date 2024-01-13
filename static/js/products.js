const categoryButtons = document.getElementsByClassName("category-btn");
const productCards = document.getElementsByClassName("product-card");
const sortButtons = document.getElementsByClassName("sort-btn");

for (let button of categoryButtons) {
  button.addEventListener("click", (e) => {
    if (e.target.dataset.category) {
      handleCategoryClick(e.target.dataset.category);
    }
  });
}

for (let button of sortButtons) {
  button.addEventListener('click' , (e) => {
    
  })
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
