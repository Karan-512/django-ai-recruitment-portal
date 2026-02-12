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


document.addEventListener("DOMContentLoaded", function () {
    previewLogo("companyLogoInput", "logoPreviewContainer");
});

document.querySelector("input[name='company_website']")
.addEventListener("blur", function () {
    if (this.value && !this.value.startsWith("http")) {
        this.value = "https://" + this.value;
    }
});

function previewLogo(inputId, previewContainerId) {
    const input = document.getElementById(inputId);
    const previewContainer = document.getElementById(previewContainerId);

    if (!input || !previewContainer) return;

    input.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        // Optional: validate file type
        if (!file.type.startsWith('image/')) {
            alert("Please select a valid image file.");
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            // Remove icon if exists
            const existingIcon = previewContainer.querySelector('i');
            if (existingIcon) existingIcon.remove();

            let img = previewContainer.querySelector('img');

            if (!img) {
                img = document.createElement('img');
                img.className = "img-fluid rounded-circle logo-img";
                previewContainer.appendChild(img);
            }

            img.src = e.target.result;
        };

        reader.readAsDataURL(file);
    });
}