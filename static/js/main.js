function togglePassword(inputId, iconWrapper) {

    const input = document.getElementById(inputId);
    const icon = iconWrapper.querySelector("i");

    if (input.type === "password") {
        input.type = "text";

        // Change to eye-slash icon
        icon.classList.remove("fi-rr-eye");
        icon.classList.add("fi-rr-eye-crossed");

    } else {
        input.type = "password";

        // Change back to eye icon
        icon.classList.remove("fi-rr-eye-crossed");
        icon.classList.add("fi-rr-eye");
    }
}
