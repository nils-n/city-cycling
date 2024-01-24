const modalBtn = document.getElementById("newsletter-btn");
const newsletterInputEl = document.getElementById("mc-embedded-subscribe");
const newsletterMailInputEl = document.getElementById("mce-EMAIL");
console.log("home js loaded");

// // make newsletter modal appear after.5
document.addEventListener("DOMContentLoaded", (e) => {
  console.log("document loaded");
  console.log("removing margins from MC form");
  console.log(newsletterInputEl.style.marginTop);

  newsletterInputEl.style.marginBottom = "0.5em";
  newsletterInputEl.style.marginTop = "0.5em";

  newsletterMailInputEl.style.marginBottom = "0.5em";
  newsletterMailInputEl.style.marginTop = "0.5em";

  console.log(newsletterInputEl.style.marginTop);
  //   setTimeout(() => {
  //     modalBtn.click();
  //     console.log("loadin modal");
  //   }, 3000);
});
