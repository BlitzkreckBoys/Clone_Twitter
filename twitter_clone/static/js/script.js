document.addEventListener('DOMContentLoaded', function () {
    // Select all elements with the class 'fa-heart' inside '.tweet-actions'
    const likeButtons = document.querySelectorAll('.tweet-actions .fa-heart');

    // Function to update the like button state
    function updateLikeButton(button, isLiked) {
        if (isLiked) {
            button.classList.add('liked');
            button.style.color = 'red'; // Set color for liked state
        } else {
            button.classList.remove('liked');
            button.style.color = ''; // Reset color for not liked state
        }
    }

    // Initialize the like buttons on page load
    likeButtons.forEach(button => {
        const isLiked = button.getAttribute('data-liked') === 'true';
        updateLikeButton(button, isLiked);

        // Add click event listener to toggle like
        button.addEventListener('click', function () {
            const tweetId = this.getAttribute('data-tweet-id');
            const isLiked = this.getAttribute('data-liked') === 'true';
            const likeCountElement = document.getElementById(`like-count-${tweetId}`);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/like_tweet/${tweetId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                updateLikeButton(this, data.liked);
                likeCountElement.textContent = data.likes_count;
                this.setAttribute('data-liked', data.liked);
            });
        });
    });

    // Add double-click event listener to tweet containers
    const tweetContainers = document.querySelectorAll('.tweet-container');
    tweetContainers.forEach(container => {
        container.addEventListener('dblclick', function () {
            const likeButton = this.querySelector('.fa-heart');
            const tweetId = likeButton.getAttribute('data-tweet-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const likeCountElement = document.getElementById(`like-count-${tweetId}`);
            
            // If the tweet is not already liked
            if (likeButton.getAttribute('data-liked') === 'false') {
                fetch(`/like_tweet/${tweetId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    updateLikeButton(likeButton, data.liked);
                    likeCountElement.textContent = data.likes_count;
                    likeButton.setAttribute('data-liked', data.liked);
                });
            }
        });
    });
});
