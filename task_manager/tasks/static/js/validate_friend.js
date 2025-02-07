document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.querySelector('input[name="friend_username"]');
    const submitButton = document.querySelector('button[name="plus_button"]');

    if (!inputField || !submitButton) {
        console.error("Input field or submit button not found.");
        return;
    }
    inputField.addEventListener("input", function() {
            submitButton.disabled = false;
            hideTooltip(inputField);
        });

    inputField.addEventListener("blur", function() {
        const username = inputField.value.trim();

        if (username.length === 0) {
            hideTooltip(inputField);
            submitButton.disabled = true;
            return;
        }

        fetch(`/tasks/friends/check_username/?username=${encodeURIComponent(username)}`)

            .then(response => {
                if (!response.ok) {
                    throw new Error("User check API failed");
                }
                return response.json();
            })
            .then(data => {
                if (!data.exists) {
                    showTooltip(inputField, "❌ User not found!");
                    submitButton.disabled = true;
                } else {
                    hideTooltip(inputField);
                    submitButton.disabled = false;
                }
            })
            .catch(error => {
                console.error("Error checking username:", error);
                showTooltip(inputField, "⚠️ Error checking user");
            });
    });

    function showTooltip(element, message) {
        hideTooltip(element);

        let tooltip = document.createElement("div");
        tooltip.className = "tooltip";
        tooltip.textContent = message;
        tooltip.style.position = "absolute";
        tooltip.style.backgroundColor = "red";
        tooltip.style.color = "white";
        tooltip.style.padding = "5px 10px";
        tooltip.style.borderRadius = "5px";
        tooltip.style.fontSize = "12px";
        tooltip.style.marginTop = "5px";
        tooltip.style.whiteSpace = "nowrap";
        tooltip.style.zIndex = "1000";

        element.parentNode.style.position = "relative";  // Ustawienie parenta na relative
        tooltip.style.left = "0";
        tooltip.style.top = "30px";  // Pozycja pod polem input

        element.parentNode.appendChild(tooltip);

        setTimeout(() => hideTooltip(element), 2000);
    }

    function hideTooltip(element) {
        let tooltip = element.parentNode.querySelector(".tooltip");
        if (tooltip) {
            tooltip.remove();
        }
    }
});
