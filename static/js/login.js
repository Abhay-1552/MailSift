function toggleForm() {
    var loginForm = document.getElementById("login-form");
    var signupForm = document.getElementById("signup-form");

    if (loginForm.classList.contains("hidden")) {
        loginForm.classList.remove("hidden");
        signupForm.classList.add("hidden");
    } else {
        loginForm.classList.add("hidden");
        signupForm.classList.remove("hidden");
    }
}