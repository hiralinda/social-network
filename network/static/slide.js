// Function to handle form submission
function handleFormSubmission(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the form data
    const formData = new FormData(event.target);

    // Send a POST request to the server
    fetch('/new_post/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token
        }
    })
    .then(response => response.json())
    .then(data => {
        // Add the new post with sliding animation
        addNewPost(`<div class="post frosted-glass mb-4 p-3" data-post-id="${data.id}">
            <p class="post-content mb-2">${data.content}</p>
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <a href="/profile/${data.author}" class="text-decoration-none">
                        <strong>${data.author}</strong>
                    </a>
                </div>
                <div>
                    <small class="text-muted">${data.created_at}</small>
                </div>
                <div>
                    <button class="btn like-button bi-heart" data-post-id="${data.id}" data-liked="false" style="border-width: 0; color: #c1121f"></button>
                    <span id="likes-count-${data.id}" class="text-muted">${data.likes} likes</span>
                </div>
            </div>
        </div>`);
        
        // Clear the form input
        document.getElementById('content').value = '';
    })
    .catch(error => console.error('Error:', error));
}

// Add event listener to the form
document.getElementById('new-post-form').addEventListener('submit', handleFormSubmission);
