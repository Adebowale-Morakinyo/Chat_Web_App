# Chat Web App

This is a simple chat web application built with Flask, Socket.IO, and SQLAlchemy.

## Project Structure

The project has the following file structure:


- `myapp/`: This directory contains the Flask application.
- `static/`: This directory contains static files, such as JavaScript and CSS.
- `templates/`: This directory contains HTML templates used by Flask to generate the web pages.
- `__init__.py`: Initializes the Flask application, SQLAlchemy, and Socket.IO.
- `config.py`: Contains the configuration settings for the Flask application.
- `database.py`: Defines the database schema using SQLAlchemy.
- `views.py`: Contains the Flask views and Socket.IO events that define the application's behavior.
- `server.py`: Runs the Flask application.
- `requirements.txt`: Lists the Python dependencies required to run the project.

## Running the Application

To run the application, follow these steps:

1. Install the required Python dependencies by running `pip install -r requirements.txt`.
2. Start the Flask application by running `python server.py`.
3. Open your web browser and navigate to `http://localhost:5000`.

## Functionality

The chat application allows users to join a chat room and send messages to each other in real-time. The application also stores messages in a SQLite database using SQLAlchemy. Users can leave the chat room at any time using the "Leave" button in the navigation bar.

## Future Enhancements

In the future, we plan to add the following enhancements:

- A homepage that includes a link to the chat room, as well as links to data visualizations built using the Pandas library.
- Data visualizations that show real-time statistics about the chat room, such as the number of active users and the frequency of messages.
- A user registration system that allows users to create accounts and login to the chat room with their username and password.
- Support for sending images and files in addition to text messages.

## Credits

This project was created by Adebowale Ifeoluwa (Me!).


### For development use, not production (simplifying development workflow)
This code is a simple chat application that uses Flask, Flask-SocketIO, and Flask-CORS on the server side, and JavaScript, HTML, and CSS on the client side. The server side is responsible for handling the communication between clients, by using the WebSocket protocol provided by SocketIO. The clients use the browser's WebSocket API to communicate with the server.

On the server side, a Flask app is created and a blueprint is registered for handling views. CORS is also set up to allow for cross-origin resource sharing. A SocketIO instance is then created, with the app and a wildcard origin. The server has one event handler that listens for a 'event' event, and when it receives one, it appends the message to a database and then emits the same message to all clients connected to the server.

On the client side, the code uses JavaScript to create an asynchronous function that appends a message to the chat window. The function takes in an image, a message, and a side argument, which can be left or right. The function also uses the fetch API to load the user's name and previous messages from the server. The code also includes several utility functions for formatting dates and getting elements from the DOM.

Finally, the client side code creates a WebSocket connection to the server using the socket.io library, and sets up event listeners for the 'connect' and 'disconnect' events, which are emitted by the server when a client connects or disconnects from the server. When the user submits a message, the message is sent to the server via the WebSocket connection.
#

Flask_cors used because of Werkzeug limitation issues I had.

## Screenshot
| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Home%20Page.PNG">  Home Page|  <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Login.PNG" > Login Page|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chatting%201.PNG"> Chatting Window 1|
|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chatting%202.PNG"> Chatting Window 2|  <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chat%20Window.PNG"> Chatting Window 3|

## Reference
[UI Chat Idea](https://codepen.io/sajadhsm/pen/odaBdd), [Chat Avatar image](https://www.flaticon.com/free-icon/chat_4575970?term=avatar+chat&page=1&position=13&origin=search&related_id=4575970)