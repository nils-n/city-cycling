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

console.log(stripePublicKey);
console.log(clientSecret);

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
