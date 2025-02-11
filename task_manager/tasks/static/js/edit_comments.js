document.addEventListener("DOMContentLoaded", function () {
    function showEditForm(commentId, content) {
        let commentText = document.getElementById(`comment-text-${commentId}`);
        let editForm = document.getElementById(`edit-form-${commentId}`);
        let editTextarea = document.getElementById(`edit-content-${commentId}`);

        if (commentText && editForm && editTextarea) {
            commentText.style.display = 'none';
            editForm.style.display = 'block';
            editTextarea.value = content;
        }
    }

    function hideEditForm(commentId) {
        let commentText = document.getElementById(`comment-text-${commentId}`);
        let editForm = document.getElementById(`edit-form-${commentId}`);

        if (commentText && editForm) {
            commentText.style.display = 'block';
            editForm.style.display = 'none';
        }
    }


    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            let commentId = this.getAttribute("data-comment-id");
            let content = this.getAttribute("data-content");
            showEditForm(commentId, content);
        });
    });


    document.querySelectorAll(".cancel-btn").forEach(button => {
        button.addEventListener("click", function () {
            let commentId = this.getAttribute("data-comment-id");
            hideEditForm(commentId);
        });
    });
});
