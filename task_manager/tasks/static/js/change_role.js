document.addEventListener("DOMContentLoaded", function () {
    console.log("JS Loaded - Change Role");

    document.querySelectorAll(".change-role-btn").forEach(button => {
        button.addEventListener("click", function () {
            let userId = this.getAttribute("data-user-id");
            let formContainer = document.getElementById("role-edit-" + userId);
            let roleDisplay = document.getElementById("role-display-" + userId);

            console.log(`Editing role for user ID: ${userId}`);

            roleDisplay.style.display = "none";
            formContainer.style.display = "inline";
            this.style.display = "none";
        });
    });

    document.querySelectorAll(".cancel-role-btn").forEach(button => {
        button.addEventListener("click", function () {
            let userId = this.getAttribute("data-user-id");
            let formContainer = document.getElementById("role-edit-" + userId);
            let roleDisplay = document.getElementById("role-display-" + userId);
            let changeRoleButton = document.querySelector(`.change-role-btn[data-user-id="${userId}"]`);

            console.log(`Canceling role change for user ID: ${userId}`);

            roleDisplay.style.display = "inline";
            formContainer.style.display = "none";
            changeRoleButton.style.display = "inline";
        });
    });

    document.querySelectorAll(".save-role-btn").forEach(button => {
        button.addEventListener("click", function () {
            let userId = this.getAttribute("data-user-id");
            let newRoleId = document.querySelector(`.role-select[data-user-id="${userId}"]`).value;
            let projectId = document.getElementById("project-id").value;

            console.log(`Saving new role for user ID: ${userId}, new role ID: ${newRoleId}`);

            fetch(`/tasks/project/${projectId}/change_member_role/${userId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ new_role: newRoleId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let roleDisplay = document.getElementById("role-display-" + userId);
                    roleDisplay.textContent = data.new_role;
                    roleDisplay.style.display = "inline";

                    let editContainer = document.getElementById("role-edit-" + userId);
                    editContainer.style.display = "none";

                    let changeRoleButton = document.querySelector(`.change-role-btn[data-user-id="${userId}"]`);
                    changeRoleButton.style.display = "inline";
                } else {
                    alert("Error: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error updating role:", error);
                alert("Something went wrong, please try again.");
            });
        });
    });
});
