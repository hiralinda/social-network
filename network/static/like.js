document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const csrftoken = getCookie('csrftoken');
            const liked = this.getAttribute('data-liked') === 'true';
            
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    liked: !liked
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.classList.remove('bi-heart');
                    this.classList.add('bi-heart-fill', 'animate-like');
                    this.classList.remove('animate-unlike');
                } else {
                    this.classList.remove('bi-heart-fill');
                    this.classList.add('bi-heart', 'animate-unlike');
                    this.classList.remove('animate-like');
                }
                this.setAttribute('data-liked', data.liked);

                document.getElementById(`likes-count-${postId}`).innerText = `${data.likes} likes`;
                setTimeout(() => {
                    this.classList.remove('animate-like', 'animate-unlike');
                }, 300);
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
