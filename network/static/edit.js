document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".edit-post").forEach((button) => {
    button.onclick = function () {
      const postDiv = this.closest(".post");
      const postId = postDiv.dataset.postId;
      const contentP = postDiv.querySelector(".post-content");
      const originalContent = contentP.innerHTML;

      const textarea = document.createElement("textarea");
      textarea.className = "form-control";
      textarea.value = originalContent;
      textarea.style.marginBottom = "5px";

      const saveButton = document.createElement("button");
      saveButton.className = "btn btn-secondary btn-sm";
      saveButton.innerHTML = "Save";

      // Replace post content with textarea and save button
      contentP.replaceWith(textarea);
      this.replaceWith(saveButton);

      saveButton.onclick = function () {
        fetch(`/edit_post/${postId}/`, {
          method: "PUT",
          body: JSON.stringify({
            content: textarea.value,
          }),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => response.json())
          .then((result) => {
            if (result.success) {
              // Replace textarea with updated content
              const updatedContentP = document.createElement("p");
              updatedContentP.className = "post-content";
              updatedContentP.innerHTML = textarea.value;

              // Create a new edit button
              const newEditButton = document.createElement("button");
              newEditButton.className = "btn btn-secondary btn-sm edit-post";
              newEditButton.innerHTML = "Edit";

              // Add the same onclick function to the new edit button
              newEditButton.onclick = button.onclick;

              textarea.replaceWith(updatedContentP);
              saveButton.replaceWith(newEditButton);
            } else {
              alert(result.error);
            }
          });
      };
    };
  });
  document.querySelectorAll(".delete-post").forEach((button) => {
    button.addEventListener("click", function () {
      const postId = this.getAttribute("data-post-id");
      const csrftoken = getCookie("csrftoken");

      if (confirm("Are you sure you want to delete this post?")) {
        fetch(`/post/${postId}/delete/`, {
          method: "DELETE",
          headers: {
            "X-CSRFToken": csrftoken,
          },
        })
          .then((response) => {
            if (response.ok) {
              const postElement = document.querySelector(
                `[data-post-id="${postId}"]`
              );
              postElement.remove();
            } else {
              console.error("Error:", response.statusText);
            }
          })
          .catch((error) => console.error("Error:", error));
      }
    });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
