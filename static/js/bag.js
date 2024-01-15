const updateLinkArray = document.getElementsByClassName("update-link");
const removeLinkArray = document.getElementsByClassName("remove-item");

// Loop over the update shopping buttons
for (let updateLink of updateLinkArray) {
  updateLink.addEventListener("click", (e) => {
    if (e.target.dataset.productId) {
      handleUpdateClick(e.target.dataset.productId);
    }
  });
}

// Loop over the remove from shopping  bag buttons
for (let removeLink of removeLinkArray) {
  removeLink.addEventListener("click", (e) => {
    if (e.target.dataset.productId) {
      // if product has no size
      if (e.target.dataset.size) {
        handleRemoveClick(e.target.dataset.productId, e.target.dataset.size);
      } else {
        handleRemoveClick(e.target.dataset.productId, false);
      }
    }
  });
}

// submit the update  item form
function handleUpdateClick(productId) {
  const quantityForm = document.getElementById(`quantity-form-${productId}`);
  quantityForm.submit();
}

// submit the remove item form
// the post request requires the csrf token
// https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
// https://forum.djangoproject.com/t/send-views-py-request-post-with-javascript/23146/8
function handleRemoveClick(productId, productSize) {
  const csrftoken = getCookie("csrftoken");
  const url = `/bag/remove/${productId}`;

  //const data = { csrfmiddlewaretoken: csrftoken, size: productSize };
  console.log("removing item", productId);
  const data = JSON.stringify({
    size: productSize,
    product_id: productId,
  });

  let response = fetch(url, {
    method: "POST",
    body: data,
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
