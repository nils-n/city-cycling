const incrementBtnArray = document.getElementsByClassName("quantity-btn");
const addToBagBtn = document.getElementById("add-to-bag-btn");
const sizeChoiceArray = document.getElementsByName("product_size");
const errorMessageEl = document.getElementById("error-message");

// check whether a button to change quantity was clicked
for (let btn of incrementBtnArray) {
  btn.addEventListener("click", (e) => {
    if (e.target.dataset.productId) {
      if (e.target.dataset.buttonType === "increment") {
        handleQuantityIncrement(e.target.dataset.productId);
      } else if (e.target.dataset.buttonType === "decrement") {
        handleQuantityDecrement(e.target.dataset.productId);
      }
    }
  });
}

//notify user if they selected no size
addToBagBtn.addEventListener("click", (e) => {
  const selectedSize = document.querySelector(
    'input[name="product_size"]:checked',
  );
  handleAddToBagClick(e, e.target.dataset.hasSizes, selectedSize);
});

// flag a warning modal that user needs to select a size before adding to bag
function handleAddToBagClick(e, hasSizes, selectedSize) {
  console.log("should not add");
  if (hasSizes === "True" && !selectedSize) {
    e.preventDefault();
    errorMessageEl.innerText =
      "Error : Product has sizes, but size was not selected";
  }
  errorMessageEl.classList.remove("hidden");
}

// handle a click on the increment button
function handleQuantityIncrement(productId) {
  let quantityInputEl = document.getElementById(`qty-${productId}`);
  let quantityValue = parseInt(quantityInputEl.value);
  let maxAllowedQuantity = 99;
  if (quantityValue < maxAllowedQuantity) {
    quantityInputEl.value = parseInt(quantityValue) + 1;
  }
}

// handle a click on the decrement button ensuring non-negative quantity
function handleQuantityDecrement(productId) {
  let quantityInputEl = document.getElementById(`qty-${productId}`);
  let quantityValue = parseInt(quantityInputEl.value);
  if (quantityValue > 0) {
    quantityInputEl.value = parseInt(quantityValue) - 1;
  }
}
