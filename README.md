# iChat Web Application

iChat is a real-time web chat application built with Flask and Socket.IO. It provides a seamless and interactive platform for users to communicate with each other through individual chat rooms.

## Project Structure

```
Chat_Web_App/
    myapp/
        static/
            images/
            auth.css
            chat.css
            index.js
            styles.css
        templates/
            auth.html
            base.html
            chat.html
            visualize.html
        __init__.py
        config.py
        database.py
        views.py
    .gitignore
    gunicorn_config.py
    README.md
    requirements.txt
    server.py
```

## Getting Started

To run the iChat web application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Chat_Web_App.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   - Create a `.env` file in the project root.
   - Add the following lines to the `.env` file:

     ```env
     SECRET_KEY=your_secret_key_here
     DATABASE_URL=sqlite:///database.db
     ```

4. Run the server:

   ```bash
   python server.py
   ```
   or 
   ```bash
   gunicorn -c gunicorn_config.py server:app
   ```


Visit `http://localhost:5000` in your web browser to access iChat.

## Features

- **User Authentication:** Secure user registration and login with password hashing.
- **Real-time Chat:** Instant messaging in individual chat rooms.
- **Dynamic Chat List:** Automatically updates the chat list with new messages.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.
- **Visualize User Registration Trends** Visualize the user registration data using Pandas and Matplotlib. This feature aims to analyze the number of users registered on the app over time and present the findings in a graphical format.

## Project Architecture

### `__init__.py`

Initialization of the Flask application, configuration, and extension setup.

### `config.py`

Configuration settings for the Flask application, including the secret key and database URI.

### `database.py`

Database models and schema definition using SQLAlchemy. Includes user, chat, and message models.

### `views.py`

Blueprint for route views, including login, registration, chat, and visualization routes.

### `gunicorn_config.py`

Gunicorn's configuration file for deployment settings.

### `server.py`

Entry point for running the server. Initializes the Flask application and Socket.IO communication events.

## ⛏️ Built With <a name = "tech_stack"></a>

<img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/><img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/><img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/><img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/><img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?&style=for-the-badge&logo=bootstrap&logoColor=white"/><img alt="FlaskSqlalchemy" src ="https://img.shields.io/badge/FlaskSQLalchemy-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white"/>

## 🤳 Screenshots <a name = "screenshots"></a>
|                                                                                                                                   |                                                                                                                                   |                                                                                                                                              |
|:---------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------:|
|  <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/register_login.png">  Register   |      <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/login_page.png" > Login      | <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/new_chat.png"> Add other users (Chat Window) |
| <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/chatting_1.png"> (Chat Window _A) | <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/chatting_2.png"> (Chat Window _B) |      <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/chatting_3.png"> (Chat Window _C)       |
| <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/chatting_4.png"> (Chat Window _D) |

## Contributing

Contributions are welcome! If you'd like to contribute to iChat, please follow the [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

