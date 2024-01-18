/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/
var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
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
const spinnerDiv = document.getElementById("spinner-div");
const spinnerBackgroundDiv = document.getElementById("spinner-bg-div");
const spinnerContainerDiv = document.getElementById("loading-spinner");

var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
  ev.preventDefault();
  card.update({ disabled: true });
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

  $.post(url, postData)
    .done(function () {
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: {
              name: $.trim(form.full_name.value),
              phone: $.trim(form.phone_number.value),
              email: $.trim(form.email.value),
              address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                state: $.trim(form.county.value),
              },
            },
          },
          shipping: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            address: {
              line1: $.trim(form.street_address1.value),
              line2: $.trim(form.street_address2.value),
              city: $.trim(form.town_or_city.value),
              country: $.trim(form.country.value),
              postal_code: $.trim(form.postcode.value),
              state: $.trim(form.county.value),
            },
          },
        })
        .then(function (result) {
          if (result.error) {
            let errorDiv = document.getElementById("card-errors");
            let html = `
              <span>${result.error.message}</span>
            `;
            errorDiv.innerHTML = html;
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
    })
    .fail(function () {
      // just reload the page, error will be in django messages
      location.reload();
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

// handle css of country field selector
let countrySelectorEl = document.querySelector("select[name='country']");

// set Country field to light gray by default
document.addEventListener("DOMContentLoaded", (event) => {
  countrySelectorEl.style.color = "#6b7280";
});

// set Country field to light gray when selecting no option
countrySelectorEl.addEventListener("change", () => {
  if (countrySelectorEl.value === "") {
    countrySelectorEl.style.color = "#aab7c4";
  } else {
    countrySelectorEl.style.color = "rgb(55,65,81)";
  }
});
