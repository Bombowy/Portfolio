document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("show-role-form").addEventListener("click", function() {
        document.getElementById("role-form-container").style.display = "block";
        this.style.display = "none"; // Ukryj przycisk
    });

    document.getElementById("hide-role-form").addEventListener("click", function() {
        document.getElementById("role-form-container").style.display = "none";
        document.getElementById("show-role-form").style.display = "block"; // Przywróć przycisk
    });

     document.querySelectorAll(".edit-role-btn").forEach(button => {
        button.addEventListener("click", function () {
            let roleId = this.getAttribute("data-role-id");
            let formContainer = document.getElementById("edit-role-form-" + roleId);
            let roleName = this.getAttribute("data-role-name");
            let inputField = document.getElementById("role-name-" + roleId);

            if (inputField) {
                inputField.value = roleName;
            }
            formContainer.style.display = "block";

        });
    });

    document.querySelectorAll(".cancel-edit-role").forEach(button => {
        button.addEventListener("click", function () {
            let roleId = this.getAttribute("data-role-id");
            let formContainer = document.getElementById("edit-role-form-" + roleId);
            formContainer.style.display = "none";
        });
    });

    });
