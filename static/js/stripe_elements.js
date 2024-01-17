/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/
console.log("entering Stripe module");

let stripePublicKey = document
  .getElementById("id_stripe_public_key")
  .textContent.slice(1, -1);

let clientSecret = document
  .getElementById("id_client_secret")
  .textContent.slice(1, -1);

var stripe = Stripe(stripePublicKey);

var elements = stripe.elements();

var style = {
  base: {
    color: "#000",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#dc3545",
    iconColor: "#dc3545",
  },
};

var card = elements.create("card", { style: style });

card.mount("#card-element");

//handle realtime validation error on the card element
card.addEventListener("change", function (event) {
  let errorDiv = document.getElementById("card-errors");
  if (event.error) {
    let html = `
      <span>${event.error.message}</span>
    `;
    errorDiv.innerHTML = html;
  } else {
    errorDiv.textContent = "";
  }
});

// Handle form submit
const csrftoken = getCookie("csrftoken");
const spinnerDiv = document.getElementById("loading-spinner");
const spinnerBackgroundDiv = document.getElementById("spinner-bg-div");
const spinnerContainerDiv = document.getElementById("loading-spinner");

var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
  ev.preventDefault();
  card.update({ disabled: true });
  $("#submit-button").attr("disabled", true);
  $("#payment-form").fadeToggle(100);
  $("#loading-overlay").fadeToggle(100);
  spinnerDiv.classList.remove("hidden");
  spinnerBackgroundDiv.classList.remove("hidden");
  spinnerContainerDiv.classList.remove("hidden");

  var safeInfo = Boolean($("#id-save-info").attr("checked"));
  var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
  var postData = {
    csrfmiddlewaretoken: csrfToken,
    client_secret: clientSecret,
    save_info: safeInfo,
  };
  var url = "/checkout/cache_checkout_data/";

  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: { card: card },
    })
    .then(function (result) {
      if (result.error) {
        var errorDiv = document.getElementById("card-errors");
        var html = `
            <span class="icon" role="alert">
            <i class="fas fa-times"></i>
            </span>
            <span>${result.error.message}</span>`;
        $(errorDiv).html(html);
        card.update({ disabled: false });
        $("#submit-button").attr("disabled", false);
        // remove the loading spinner
        spinnerDiv.classList.add("hidden");
        spinnerBackgroundDiv.classList.add("hidden");
        spinnerContainerDiv.classList.add("hidden");
      } else {
        if (result.paymentIntent.status === "succeeded") {
          form.submit();
        }
      }
    });
});

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
