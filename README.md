# Social Network

[This project](https://cs50.harvard.edu/web/2020/projects/4/network/) is a part of the CS50 Web Programming with Python and JavaScript course. A social network application that allows users to make posts, follow other users, and like posts. Built using Django, JavaScript, HTML, and Bootstrap for the layout.

## Video Preview

[Video Link](https://youtu.be/SPhftAeJhBU)

## Features

- User registration and login
- Create, edit, and delete posts
- Follow and unfollow users
- Like and unlike posts
- Pagination for viewing posts
- Profile pages for each user

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Bootstrap for styling

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd social-network

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

4. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

5. **Access the application**:
    Open your browser and go to `http://127.0.0.1:8000/`.

### Usage

1. Use the **Register** link to create a new account.
2. Log in with your credentials.
3. Create new posts from the main page.
4. View all posts, posts from followed users, and individual user profiles.
5. Edit or delete your own posts.
6. Follow or unfollow users, and like/unlike posts.

## URL Configuration

- **/login**: Renders the login form.
- **/logout**: Logs the user out and redirects to the index page.
- **/register**: Displays the registration form for new users.
- **/all_posts**: Shows all posts made by users.
- **/following**: Displays posts from users that the current user follows.
- **/profile/<username>**: Displays the selected user's profile and their posts.

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Django
- **Database**: SQLite3 (or any configured database)

## Future Improvements

- **Notifications**: Implement notifications for new followers or likes.
- **Search Functionality**: Allow users to search for posts or users.
- **Enhanced User Profiles**: Add profile pictures and bio sections.
- **Direct Messaging**: Implement a messaging feature for users to communicate privately.

---

*[This project](https://cs50.harvard.edu/web/2020/projects/4/network/) is a part of the CS50 Web Programming with Python and JavaScript course.*
