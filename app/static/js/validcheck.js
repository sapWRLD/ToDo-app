const username = document.querySelector("#username");
const username_error = document.querySelector("#UsernameHelpBlock");
const password = document.querySelector("#password");
const password_error = document.querySelector("#passwordHelpBlock");
const form = document.querySelector("form");

function isUsernameValid() {
    return username.value.trim().length >= 2;
}

function isPasswordValid() {
    return password.value.length >= 8 && password.value.length <= 20;
}

// On input: only fix border if valid
username.addEventListener("input", () => {
    if (isUsernameValid()) {
        username.classList.remove("error-border");
        username_error.classList.remove("active");
    }
});

password.addEventListener("input", () => {
    if (isPasswordValid()) {
        password.classList.remove("error-border");
        password_error.classList.remove("active");
    }
});

// On submit: show errors if invalid
form.addEventListener("submit", (e) => {
    let valid = true;

    if (!isUsernameValid()) {
        username.classList.add("error-border");
        username_error.classList.add("active");
        valid = false;
    }

    if (!isPasswordValid()) {
        password.classList.add("error-border");
        password_error.classList.add("active");
        valid = false;
    }

    if (!valid) {
        e.preventDefault(); // block submission
    }
});
