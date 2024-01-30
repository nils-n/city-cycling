const successToastEl = document.getElementById("toast-success");
const errorToastEl = document.getElementById("toast-danger");
const infoToastEl = document.getElementById("toast-info");
const warningToastEl = document.getElementById("toast-warning");

// add a timeout of 5s to the toasts
if (successToastEl) {
  setTimeout(() => {
    successToastEl.classList.add("hidden");
  }, 5000);
}

if (errorToastEl) {
  setTimeout(() => {
    errorToastEl.classList.add("hidden");
  }, 5000);
}

if (infoToastEl) {
  setTimeout(() => {
    infoToastEl.classList.add("hidden");
  }, 5000);
}

if (warningToastEl) {
  setTimeout(() => {
    warningToastEl.classList.add("hidden");
  }, 5000);
}
