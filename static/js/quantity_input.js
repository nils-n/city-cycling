console.log("asdadaw");

const incrementBtnArray = document.getElementsByClassName("quantity-btn");

// check whether a button to change quantity was clicked
for (let btn of incrementBtnArray) {
  btn.addEventListener("click", (e) => {
    if (e.target.dataset.productId) {
      if (e.target.dataset.buttonType === "increment") {
        handleQuantityIncrement(
          e.target.dataset.productId,
          e.target.dataset.buttonType,
        );
      } else if (e.target.dataset.buttonType === "decrement") {
        handleQuantityDecrement(
          e.target.dataset.productId,
          e.target.dataset.buttonType,
        );
      }
    }
  });
}

// handle a click on the increment button
function handleQuantityIncrement(productId, btnType) {
  let quantityInputEl = document.getElementById(`qty-${productId}`);
  let quantityValue = parseInt(quantityInputEl.value);
  let maxAllowedQuantity = 99;
  if (quantityValue < maxAllowedQuantity) {
    quantityInputEl.value = parseInt(quantityValue) + 1;
  }
}

// handle a click on the decrement button ensuring non-negative quantity
function handleQuantityDecrement(productId, btnType) {
  let quantityInputEl = document.getElementById(`qty-${productId}`);
  let quantityValue = parseInt(quantityInputEl.value);
  if (quantityValue > 0) {
    quantityInputEl.value = parseInt(quantityValue) - 1;
  }
}
