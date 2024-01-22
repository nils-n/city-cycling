// handle css of country field selector
let countrySelectorEl = document.querySelector(
  "select[name='default_country']",
);
const rateProductBtnArray = document.getElementsByClassName("rate-product-btn");
const submitCommentBtnArray = document.getElementsByClassName(
  "comment-product-btn",
);

// Event Listeners for Rating
for (let rateBtn of rateProductBtnArray) {
  rateBtn.addEventListener("click", (e) => {
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

// Event Listeners for Submit Comment Buttons
for (let commentBtn of submitCommentBtnArray) {
  commentBtn.addEventListener("click", (e) => {
    if (
      e.target.dataset.productId &&
      e.target.dataset.userId &&
      e.target.dataset.textareaId
    ) {
      handleSubmitCommentClick(
        e.target.dataset.productId,
        e.target.dataset.userId,
        e.target.dataset.textareaId,
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
// submit the rating via a post request
// the post request requires the csrf token
// https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
// https://forum.djangoproject.com/t/send-views-py-request-post-with-javascript/23146/8

function handleRatingClick(productId, userId, rating) {
  console.log("productId, userId, rating", productId, userId, rating);
  const csrftoken = getCookie("csrftoken");
  const url = `/products/rate/${productId}`;

  const data = JSON.stringify({
    headline: "productRating",
    tag: "productRating",
    rating: `${rating}`,
    productId: `${productId}`,
    userId: `${userId}`,
  });

  let response = fetch(url, {
    method: "POST",
    body: data,
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  }).then(() => {
    //reload the page
    location.reload();
  });
}

// handle action when user clicks on a submitting a comment
// submit the comment via a post request
// the post request requires the csrf token
// https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
// https://forum.djangoproject.com/t/send-views-py-request-post-with-javascript/23146/8
function handleSubmitCommentClick(productId, userId, textareaId) {
  console.log(productId, userId, textareaId);
  const csrftoken = getCookie("csrftoken");
  const url = `/products/comment/${productId}`;
  const commentText = document.getElementById(textareaId).value;

  const data = JSON.stringify({
    headline: "productComment",
    tag: "productComment",
    comment: `${commentText}`,
    productId: `${productId}`,
    userId: `${userId}`,
  });

  let response = fetch(url, {
    method: "POST",
    body: data,
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  }).then(() => {
    //reload the page
    location.reload();
  });
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
