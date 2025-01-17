document.addEventListener("DOMContentLoaded", function () {
    // Find all links with the class 'delete-link'
    const deleteLinks = document.querySelectorAll("a.delete-link");

    // Add a 'click' event listener to each link
    deleteLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            // Display a confirmation dialog before deleting
            const confirmDelete = confirm("Are you sure you want to delete this task?");
            if (!confirmDelete) {
                event.preventDefault(); // Cancel the delete action if the user clicks 'Cancel'
            }
        });
    });
});
